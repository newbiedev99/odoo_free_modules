# -*- coding: utf-8 -*-
from odoo import models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_line_import(self):
        action = self.env.ref('import_sale_purchase_picking_line.action_line_import_wizard').read()[0]
        action.update({'views': [[False, 'form']]})
        return action
