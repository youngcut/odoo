# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import Warning
from odoo.tools.translate import _
from odoo.http import request
from html import escape
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class VoucherTemplate(models.Model):
	_name = 'voucher.template'
	_description = 'Voucher Template'

	_sql_constraints = [
		('name', 'UNIQUE(name)', "Coupon name already exist.")
	]

	name = fields.Char('Name')
	product_id = fields.Many2one('product.product','Discount-Product', domain = [('type', '=', 'service'),('is_discount_product', '=', True)])
	active = fields.Boolean('Active',default=True)

	prefix = fields.Char("Voucher Name")
	prefix_choose = fields.Boolean("Choose Prefix")
	
	amount = fields.Float (string='Coupon Amount')
	amount_choose = fields.Selection([
		('amount': 'Drawer can change the amount'),
		('amount': 'Drawer can change the amount and the type')
		('amount': "Drawer can't change the amount"),
	] string="Choose Amount")
	amount_limit = fields.Float(string='Limit the amount for the drawer')

	amount_type = fields.Selection([('fix','Fixed'),('per','%')],default='fix')
	
	min_amount = fields.Float("Minimal Amount")
	max_amount = fields.Float("Maximum Amount")

	#Validation
	product_valid = fields.Many2many('product.product', String='Valid for Specific Products')
	partner_id = fields.Many2many('res.partner')
	start_date = fields.Date("Start Date", default=fields.Date.context_today)
	expiry_date = fields.Date("Expiry Date")
	is_voucher_limit = fields.Boolean('Set Limit', default=False)
	voucher_limit = fields.Integer('Apply Limit', default="1")

	#Information
	description = fields.Text('Note')

	user_id = fields.Many2one('res.users' ,'Created By', default = lambda self: self.env.user)
	