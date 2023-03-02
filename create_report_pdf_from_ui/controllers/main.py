from odoo import http
from odoo.http import request
import os
import jinja2
import sys
import json

if hasattr(sys, 'frozen'):
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'static/src'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.create_report_pdf_from_ui', "static/src")

jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps

editor_template = jinja_env.get_template('template/tinymce.html')


class ReportPdfFromUi(http.Controller):
    
    @http.route(['/create-report-template'], type='http', auth='none', csrf=False, cors='*')
    def create_report_template(self):
        return editor_template.render({
            'title': 'Percobaan Jinja2'
        })