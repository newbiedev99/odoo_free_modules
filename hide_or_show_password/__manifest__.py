{
    'name': 'Hide Or Show Password',
    'version': '14.0.2.0.0',
    'summary': """
        Show and Hide fields by typing a password, login form, signup form, user change password
    """,
    'author': 'Newbie Dev',
    'website': 'https://agvenmuharisrifqi.github.io',
    'license': 'AGPL-3',
    'category': 'Custom/Custom',
    'depends': [
        'web', 'base', 'auth_signup'
    ],
    'data': [
        'assets/assets.xml',
        'views/login_signup.xml',
    ],
    'qweb': [
        'static/src/xml/profile.xml',
    ],
    'installable': True,
    'images':  ['static/description/banner.png'],
}