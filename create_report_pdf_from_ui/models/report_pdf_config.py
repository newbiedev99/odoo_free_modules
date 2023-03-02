from odoo import models, fields, api, _
from odoo.addons.base.models.report_paperformat import PAPER_SIZES
import re


class ReportPdfConfig(models.Model):
    _name = 'report.pdf.config'
    _description = 'Configuration Report PDF'

    name = fields.Char('Name', copy=False, required=True)
    model = fields.Char('Model Name', copy=False, required=True) 
    format = fields.Selection([(ps['key'], ps['description']) for ps in PAPER_SIZES], 'Paper size', default='A4', help="Select Proper Paper size")
    page_height = fields.Integer('Page height (mm)', default=False)
    page_width = fields.Integer('Page width (mm)', default=False)
    orientation = fields.Selection([
        ('Landscape', 'Landscape'),
        ('Portrait', 'Portrait')
        ], 'Orientation', default='Portrait')
    margin_top = fields.Float('Top Margin (mm)')
    margin_bottom = fields.Float('Bottom Margin (mm)')
    margin_left = fields.Float('Left Margin (mm)')
    margin_right = fields.Float('Right Margin (mm)')
    report_id = fields.Many2one('ir.actions.report', string='Report', copy=False)
    paperformat_id = fields.Many2one('report.paperformat', string='Paperformat', copy=False)
    report_layout = fields.Html('Report Layout')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
    ], default='draft')
    there_is_a_report_layout = fields.Char(compute='_compute_there_is_a_report_layout', string='There is a Report Layout')
    
    _sql_constraints = [
        ('name_report_uniq', 'unique(name)', 'The name of the config must be unique, as it will be used as a prefix for the report template and paperformat. !')
    ]


    def _normal_field(self, layout):
        result = layout
        fields = re.findall('\{\s?\w*\s?\}', layout)
        for field in fields:
            variable = re.search('\{\s*?(\w*\.?\w*)\s*?\}', field)
            variable = variable.group(1)
            replace = '<span t-field="{}" />'.format(variable)
            result = re.sub(field, replace, result)
        return result

    @api.depends(
        'report_layout',
    )
    def _compute_there_is_a_report_layout(self):
        for rec in self:
            if rec.report_layout:
                rec.there_is_a_report_layout = True
                
                # Normal Field such as Char, Integer, Float, Many2one(Char, Integer, Float)
                result_layout = rec._normal_field(rec.report_layout)
                print(type(result_layout))
                print(result_layout)
                print('REPORT LAYOUT => ', rec.report_layout)
            else:
                rec.there_is_a_report_layout = False

    def create_edit_report_layout(self):
        self.ensure_one()
        return {
            'name': 'Create Report Layout',
            'type': 'ir.actions.client',
            'tag': 'create_report_pdf_from_ui_editor_template',
            'target': 'main',
            'params': {
                'active_id': self.id,
                'model_name': 'report.pdf.config',
            }
        }

    def set_to_draft(self):
        if self.state != 'draft':
            self.state = 'draft'

    def set_to_active(self):
        if self.state != 'active':
            self.state = 'active'
    
