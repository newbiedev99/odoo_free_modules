from odoo import models, fields, api, _
from odoo.exceptions import UserError, MissingError
import json


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    create_inv_from = fields.Selection([
        ('sale_order', 'Sale Order'),
        ('delivery_order', 'Delivery Order'),
    ], string='Invoice From', required=True, default='sale_order')
    delivery_order_ids = fields.Many2many(
        comodel_name='stock.picking', 
        relation='sale_advance_payment_inv_stock_picking',
        string='Delivery'
    )
    delivery_order_ids_domain = fields.Char(compute='_compute_delivery_order_ids_domain', string='Delivery Order Domain')
    
    def _get_delivery_invoice(self):
        delivery_invoice = []
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for sale_invoice_id in sale_orders.invoice_ids:
            if sale_invoice_id.state != 'cancel':
                for delivery_id in sale_invoice_id.delivery_ids:
                    delivery_invoice.append(delivery_id.id)
        return list(set(delivery_invoice))


    @api.depends('create_inv_from')
    def _compute_delivery_order_ids_domain(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        delivery_invoice = self._get_delivery_invoice()
        for rec in self:
            if rec.create_inv_from == 'delivery_order':
                rec.delivery_order_ids_domain = json.dumps(
                    [('sale_id.id', '=', sale_orders.id), ('state', '=', 'done'), ('id', 'not in', delivery_invoice), ('origin', 'not ilike', 'Return of')]
                )
            elif rec.create_inv_from != 'delivery_order':
                rec.delivery_order_ids_domain = json.dumps(
                    [('origin', '=', sale_orders.name), ('state', '=', 'done'), ('id', 'not in', delivery_invoice), ('origin', 'not ilike', 'Return of')]
                )

    def create_invoices(self):
        if self.create_inv_from == 'delivery_order' and not self.delivery_order_ids:
            raise MissingError(_('You must enter the selected Delivery Order if you are creating an Invoice from a Delivery Order'))
        
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if self.advance_payment_method == 'delivered':
            delivery_ids = []
            create_from_do = False
            if self.create_inv_from == 'sale_order':
                delivery_invoice = self._get_delivery_invoice()
                delivery_ids = [delivery_id.id for delivery_id in sale_orders.picking_ids if delivery_id.state == 'done' and delivery_id.id not in delivery_invoice and delivery_id.is_return == False]
            else:
                create_from_do = True
                delivery_ids = [delivery_id.id for delivery_id in self.delivery_order_ids]
            sale_orders.with_context(delivery_ids=delivery_ids,create_from_do=create_from_do)._create_invoices(final=self.deduct_down_payments)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                amount, name = self._get_advance_details(order)

                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                tax_ids = order.fiscal_position_id.map_tax(taxes).ids
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

                so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
                so_line = sale_line_obj.create(so_line_values)
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}