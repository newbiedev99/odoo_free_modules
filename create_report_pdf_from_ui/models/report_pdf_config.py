from odoo import models, fields, api, _
from odoo.addons.base.models.report_paperformat import PAPER_SIZES
import re


class ReportPdfConfig(models.Model):
    _name = 'report.pdf.config'
    _description = 'Configuration Report PDF'

    def _get_default_template(self):
        return '<div class="paper"><div class="editor"></div></div>'

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
    report_layout = fields.Html('Report Layout', default=lambda self: self._get_default_template())
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
    ], default='draft')
    
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

    def create_edit_report_layout(self):
        self.ensure_one()
        self.with_context(report_active_id=self.id)
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/create-report-template?id=%s' % (self.id),
        }

    def set_to_draft(self):
        if self.state != 'draft':
            self.state = 'draft'

    def set_to_active(self):
        if self.state != 'active':
            self.state = 'active'
    
