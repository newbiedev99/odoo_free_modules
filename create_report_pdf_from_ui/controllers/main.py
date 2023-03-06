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
    
    report_id = 1

    @http.route(['/create-report-template'], type='http', auth='none', csrf=False)
    def create_report_template(self, **kwargs):
        report_config = request.env['report.pdf.config'].sudo().browse(self.report_id)
        x = requests.get(
            url='http://localhost:8099/get-report-data'
        )
        print(x.headers)
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
                data = dict(
                    berhasil = True
                )
                data_request = json.loads(request.httprequest.data)
                report_config.write({
                    'report_layout': data_request.get('report_layout', report_config.report_layout)
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
        
        # print('DI SINIIIIIIIIIII')
        # data = json.dumps({
        #     'status': 'pass',
        # })
        # return data
            # return json.dumps(res)
        # if request.httprequest.method == 'POST':
        #     return json.dumps({'success': True, 'status': 200})

    