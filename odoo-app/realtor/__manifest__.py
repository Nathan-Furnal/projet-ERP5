# -*- coding: utf-8 -*-
{
    'name': "Realtor",

    'summary': """
        A real estate management app.""",

    'description': """
        A real estate management app with interaction between apartments and buyers.
    """,

    'author': "Nathan Furnal",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/realtor_apartment_views.xml',
        'views/realtor_offer_views.xml',
        'views/res_users_views.xml',
        'views/realtor_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
}
