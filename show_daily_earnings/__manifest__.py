# -*- coding: utf-8 -*-
{
    'name': "Show Daily Earnings",

    'summary': """
        Shows daily earning at the right corner of point of sales.""",

    'description': """
    """,

    'author': "Youngcut",
    'website': "https://github.com/youngcut",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'point_of_sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    "images": [
        'static/description/screenshot_daily.png'
    ],
    'qweb': [
        'static/src/xml/pos.xml'
     ]
}