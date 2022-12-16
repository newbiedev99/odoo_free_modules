{
    "name": "Widget Number",
    "summary": """
        Widget Comma in Number Field
    """,
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "Newbie Dev",
    "website": "https://agvenmuharisrifqi.github.io",
    "depends": ["web"],
    "data": [
        'tests/ir.model.access.csv',
        'tests/train_widget.xml',
    ],
    "assets": {
        "web.assets_backend": [
            'number_widget/static/src/js/comma_input.js',
        ],
    },
    "installable": True,
}