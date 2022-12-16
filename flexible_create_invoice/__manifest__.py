{
    'name': 'Flexible Create Invoice',
    'version': '15.0.1.0.0',
    'summary': 'Can Create Invoices from Delivery Order or Sale Order',
    'author': 'Newbie Dev',
    'website': 'https://agvenmuharisrifqi.github.io',
    'license': 'AGPL-3',
    'category': 'Sales/Sales',
    'depends': [
        'base', 'sale', 'account', 'sale_stock', 'web_domain_field', 'stock'
    ],
    'data': [
        'wizard/sale_advance_inherit.xml',

        'views/sale_order_inherit.xml',
        'views/account_move_inherit.xml',
        'views/stock_picking.xml',
    ],
    'images': [
        'static/description/create_invoice.png',
    ],
    'demo': [],
    'auto_install': False,
    'application': True,
    'assets': {}
}