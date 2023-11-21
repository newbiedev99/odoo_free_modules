# -*- coding: utf-8 -*-
{
    "name": "Import Purchase/Sale/Picking Line",
    'summary': 'Import Purchase/Sale/Picking Line',
    'description': """Import Purchase/Sale/Picking Line""",
    "version":"14.0.1.0",
    "category": "Custom/Custom",
    'author': 'Newbie Dev',
    'website': '',
    "depends": ['stock', 'sale', 'purchase'],
    "data": [
        'security/ir.model.access.csv',
        
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',

        'wizard/line_import_wizard.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}