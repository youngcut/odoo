# -*- coding: utf-8 -*-
{
    'name': "POS Sales History",

    'summary': """
        See a quick overview of all products for each customer and where bought it (POS/Online).""",

    'description': """
    """,

    'author': "Microman",
    'website': "https://github.com/youngcut",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'point_of_sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    "images": [
        'static/description/screenshot.jpg'
    ],
    'license': "LGPL-3"
}