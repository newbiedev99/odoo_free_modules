from odoo import models, fields, api, _
from random import randint
from odoo.exceptions import MissingError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    unique_line = fields.Integer('Unique Line')
    
    @api.onchange('unique_line')
    def _onchange_unique_line(self):
        unique = []
        for order_line in self.order_id.order_line:
            unique.append(order_line.unique_line)
        unique_number = randint(1,9999999)
        while unique_number in unique:
            unique_number = randint(1, 9999999)
        self.unique_line = unique_number

    def _prepare_invoice_line_do(self, quantity_do=0):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        return {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': quantity_do,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }

    # Send Unique Line Stock Move in DO
    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
        res.update({'unique_line': self.unique_line})
        return res

    