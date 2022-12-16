from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    invoice_number = fields.Char('No. Invoice')


class StockRule(models.Model):
    _inherit = 'stock.rule'

    # Get Unique Line Stock Move from SO
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        res = super(StockRule, self)._get_stock_move_values(product_id=product_id, product_qty=product_qty, product_uom=product_uom, location_id=location_id, name=name, origin=origin, company_id=company_id, values=values)
        if values.get('unique_line', False):
            res['unique_line'] = values.get('unique_line', 0)
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    unique_line = fields.Integer('Unique Line')
