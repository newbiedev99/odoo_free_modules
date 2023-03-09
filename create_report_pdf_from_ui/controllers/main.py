from odoo import http
from odoo.http import request
import requests
import os
import jinja2
import sys
import json
from werkzeug import Response

if hasattr(sys, 'frozen'):
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'static/src'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.create_report_pdf_from_ui', "static/src")

jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps

editor_template = jinja_env.get_template('template/tinymce.html')


class ReportPdfFromUi(http.Controller):
    
    report_id = None

    @http.route(['/create-report-template'], type='http', auth='none', csrf=False)
    def create_report_template(self, id, **kwargs):
        self.report_id = int(id)
        report_config = request.env['report.pdf.config'].sudo().browse(self.report_id)
        return editor_template.render({
            'title': report_config.name,
            'report_layout': report_config.report_layout
        })
    
    @http.route('/get-report-data', type='http', auth='none', csrf=False, methods=['GET', 'POST'])
    def get_report_data(self, **kwargs):
        data = False
        report_config = request.env['report.pdf.config'].sudo().browse(self.report_id)
        try:
            if request.httprequest.method == 'GET':
                data = dict(
                    paper_size = report_config.format,
                    orientation = report_config.orientation,
                    page_height = report_config.page_height,
                    page_width = report_config.page_width,
                    margin_left = report_config.margin_left,
                    margin_right = report_config.margin_right,
                    margin_top = report_config.margin_top,
                    margin_bottom = report_config.margin_bottom,
                )
            if request.httprequest.method == 'POST':
                action_id = request.env.ref('create_report_pdf_from_ui.report_pdf_config_action')
                data = dict(
                    redirect_link = '/web#action=%s&model=report.pdf.config&view_type=form&id=%s' % (action_id.id, report_config.id)
                )
                print(data)
                data_request = json.loads(request.httprequest.data)
                report_config.write({
                    'report_layout': data_request.get('report_layout', report_config.report_layout),
                    'margin_top': data_request.get('margin_top', report_config.margin_top),
                    'margin_bottom': data_request.get('margin_bottom', report_config.margin_bottom),
                    'margin_left': data_request.get('margin_left', report_config.margin_left),
                    'margin_right': data_request.get('margin_right', report_config.margin_right),
                })
            return request.make_response(
                data = json.dumps({
                    'method': request.httprequest.method,
                    'status': 200,
                    'data': data
                }),
                headers = [
                    ('Content-Type', 'application/json; charset=utf-8') 
                ]
            )
        except:
            return request.make_response(
                data = json.dumps({
                    'method': request.httprequest.method,
                    'status': 400,
                    'data': data
                }),
                headers = [
                    ('Content-Type', 'application/json; charset=utf-8') 
                ]
            )
    
    def generate_link_redirect(self):
        pass