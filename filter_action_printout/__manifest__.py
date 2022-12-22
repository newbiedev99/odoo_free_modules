{
    'name': 'Filter Action Printout',
    'version': '15.0.1.0.0',
    'summary': 'Filter printout actions for visible and invisible',
    'author': 'Newbie Dev',
    'website': 'https://agvenmuharisrifqi.github.io',
    'license': 'AGPL-3',
    'category': 'Custom/Custom',
    'depends': [
        'base', 'web'
    ],
    'data': [
        'views/ir_actions_report.xml',
    ],
    "installable": True,
    'images': [
        'static/description/after_filter.png',
    ],
    'assets': {
        'web.assets_backend': [
            'filter_action_printout/static/src/js/action_menus.js',
        ],
    }
}