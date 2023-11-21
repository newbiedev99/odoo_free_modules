# -*- coding: utf-8 -*-
from odoo.exceptions import Warning
from odoo import models, fields, exceptions, api, _
from odoo.exceptions import MissingError
import io
import tempfile
import binascii
import logging

_logger = logging.getLogger(__name__)
try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')

class LineImportWizard(models.TransientModel):
    _name = 'line.import.wizard'

    data_file = fields.Binary(string='XLS File')
    file_name = fields.Char('Filename')

    def download_example(self):
        active_model = self.env.context.get('active_model')
        if active_model == 'stock.picking':
            file_exam = 'line_picking_exam.xlsx'
        if active_model == 'sale.order':
            file_exam = 'line_sale_exam.xlsx'
        if active_model == 'purchase.order':
            file_exam = 'line_purchase_exam.xlsx'
        return {
            'type' : 'ir.actions.act_url',
            'url': f'/import_sale_purchase_picking_line/static/src/{file_exam}',
            'target': 'new',
        }

    def action_import(self):
        active_model = self.env.context.get('active_model')
        if not self.file_name:
            return False
        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix='.xslx')
            fp.write(binascii.a2b_base64(self.data_file))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
        except Exception:
            raise MissingError(_('Invalid file!'))
        
        reader = []
        keys = sheet.row_values(0)
        values = [sheet.row_values(i) for i in range(1, sheet.nrows)]
        
        for value in values:
            reader.append(dict(zip(keys, value)))

        if len(reader) == 0:
            raise MissingError(_('No importable values'))

        for idx, read in enumerate(reader):
            if read['product_reference'] == '':
                raise MissingError(_(f'product_reference empty at line {idx + 1}'))
            
            if read['product_qty'] < 0:
                raise MissingError(_(f'product_qty less than 0 at line {idx + 1}'))
            
            if read['product_qty'] == '':
                raise MissingError(_(f'product_qty empty at line {idx + 1}'))
            
            if read['price_unit'] < 0 and active_model in ['purchase.order']:
                raise MissingError(_(f'price_unit less than 0 at line {idx + 1}'))
            
            if read['price_unit'] == '' and active_model in ['purchase.order']:
                raise MissingError(_(f'price_unit empty at line {idx + 1}'))
        
        if active_model == 'stock.picking':
            result = self.import_picking_line(reader)
        if active_model == 'sale.order':
            result = self.import_sale_line(reader)
        if active_model == 'purchase.order':
            result = self.import_purchase_line(reader)

        if result:
            attachment_ids = self.env['ir.attachment'].sudo().create({
                'name': self.file_name,
                'type': 'binary',
                'datas': self.data_file,
                'res_model': active_model,
                'res_id': result.id,
                'res_name': self.file_name,
                'public' : True
            })
            self.env['mail.message'].sudo().create({
                'body': _('<p>Attached Files : </p>'),
                'model': active_model,
                'message_type': 'comment',
                # 'no_auto_thread': False,
                'res_id': result.id,
                'attachment_ids': [(6, 0, attachment_ids.ids)],
            })

        return True
    
    def import_picking_line(self, reader_line=[]):
        picking_id = self.env['stock.picking'].browse(self.env.context.get('active_id'))

        move = self.env['stock.move']
        for line in reader_line:
            product_id = self.env['product.product'].search([('default_code', '=', line['product_reference'])], limit=1)
            product_uom_qty = int(line['product_qty'])
            if not product_id or not product_id.uom_id:
                raise MissingError(_('Product or UoM Product not found'))
            vals = {
                'name': (product_id.display_name or '')[:2000],
                'product_id': product_id.id,
                'date': picking_id.scheduled_date,
                'date_deadline': picking_id.scheduled_date,
                'location_id': picking_id.location_id.id,
                'location_dest_id': picking_id.location_dest_id.id,
                'picking_id': picking_id.id,
                'partner_id': picking_id.partner_id.id,
                'state': 'draft',
                'company_id': picking_id.company_id.id,
                'picking_type_id': picking_id.picking_type_id.id,
                'warehouse_id': picking_id.picking_type_id.warehouse_id.id,
                'product_uom_qty': product_uom_qty,
                'product_uom': product_id.uom_id.id,
            }
            move |= self.env['stock.move'].create(vals)

        if move:
            return move.picking_id

    def import_purchase_line(self, reader_line=[]):
        purchase_id = self.env['purchase.order'].browse(self.env.context.get('active_id'))

        order_line = self.env['purchase.order.line']
        for line in reader_line:
            product_id = self.env['product.product'].search([('default_code', '=', line['product_reference'])], limit=1)
            product_qty = int(line['product_qty'])
            price_unit = float(line['price_unit'])
            if not purchase_id.date_planned:
                raise MissingError(_('You must fill in the Receipt Date first'))
            if not product_id or not product_id.uom_id:
                raise MissingError(_('Product or UoM Product not found'))
            vals = {
                'name': (product_id.display_name or '')[:2000],
                'product_id': product_id.id,
                'date_planned': purchase_id.date_planned,
                'price_unit': price_unit,
                'product_qty': product_qty,
                'product_uom': product_id.uom_id.id,
                'company_id': purchase_id.company_id.id,
                'order_id': purchase_id.id,
            }
            order_line |= self.env['purchase.order.line'].create(vals)

        if order_line:
            return order_line.order_id
        
    def import_sale_line(self, reader_line=[]):
        sale_id = self.env['sale.order'].browse(self.env.context.get('active_id'))

        order_line = self.env['sale.order.line']
        for line in reader_line:
            product_id = self.env['product.product'].search([('default_code', '=', line['product_reference'])], limit=1)
            product_uom_qty = int(line['product_qty'])
            price_unit = float(line['price_unit'])
            if not product_id or not product_id.uom_id:
                raise MissingError(_('Product or UoM Product not found'))
            vals = {
                'name': (product_id.display_name or '')[:2000],
                'product_id': product_id.id,
                'price_unit': price_unit,
                'product_uom_qty': product_uom_qty,
                'product_uom': product_id.uom_id.id,
                'company_id': sale_id.company_id.id,
                'order_id': sale_id.id,
            }
            order_line |= self.env['sale.order.line'].create(vals)

        if order_line:
            return order_line.order_id
