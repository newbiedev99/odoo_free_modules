{
    'name': 'Create Report PDF From UI',
    'version': '15.0.1.0.0',
    'description': 'Module for Create Report PDF From UI',
    'summary': """
        This module can help you create PDF reports quickly, and can be used by people who don't understand HTML and CSS.
    """,
    'author': 'Newbie Dev',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Custom/Custom',
    'depends': [
        'web', 'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/report_pdf_config.xml',
        'views/report_so.xml',
    ],
    'demo': [],
    'auto_install': False,
    'application': True,
    'assets': {}
}