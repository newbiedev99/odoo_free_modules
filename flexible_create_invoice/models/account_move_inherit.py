from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_ids = fields.Many2many('stock.picking', relation='account_move_stock_picking', string='DO/GR')
    invoice_do_flag = fields.Boolean(compute='_compute_invoice_do_flag', string='Invoice DO Flag')
    
    @api.depends('delivery_ids', 'state')
    def _compute_invoice_do_flag(self):
        def change_invoice_number(delivery_id, name):
            for delivery in delivery_id:
                delivery.invoice_number = name
            
        for rec in self:
            if rec.move_type in ['out_invoice', 'in_invoice'] and rec.state != 'cancel':
                change_invoice_number(rec.delivery_ids, rec.name)
                rec.invoice_do_flag = True
            else:
                change_invoice_number(rec.delivery_ids, False)
                rec.invoice_do_flag = False
    