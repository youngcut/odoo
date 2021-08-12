# -*- coding: utf-8 -*-
{
	'name': 'Website Voucher Suite',
	'summary': 'Create vouchers for websites with ease.',
	'description': """
		Manage the coupons in your sales module. The vouchers can be used in website.
		Each voucher can be limited by customer, price, products, date and quantity.
		You can also choose between fix-price or percentage.
	""",
	"category": 'Sales',
	'author': 'Youngcut',
	'version' : '1.0.0.0',
	'website': 'https://github.com/youngcut/odoo',
	'depends': ['base','sale', 'website_sale'],
	'data': [
		'security/ir.model.access.csv',
		'views/voucher.xml',
		'views/voucher_web.xml',
		'views/views.xml'
	],

    'images': ['static/description/screenshot_frontend.png'],
	'installable': True,
}
