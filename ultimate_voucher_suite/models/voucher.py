# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import Warning
from odoo.tools.translate import _
from odoo.http import request
from html import escape
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import random

class Voucher(models.Model):
	_name = 'voucher'
	_description = 'Voucher Items'

	_sql_constraints = [
		('coupon_code', 'UNIQUE(coupon_code)', "Coupon code already exist."),
		('name', 'UNIQUE(name)', "Coupon name already exist.")
	]

	@api.constrains('amount','start_date','expiry_date','max_amount', 'amount_type')
	def _check_config(self):

		if self.amount_type == 'fix':
			if self.max_amount and self.amount:
				if self.amount > self.max_amount:
					raise Warning(_( "Coupon amount is greater than maximum amount"))

		if self.expiry_date and self.start_date:
			if self.expiry_date < self.start_date:
				raise Warning(_( "Please Enter Valid Date. Expiry Date should not be greater than Start Date."))

		if self.amount == 0:
			raise Warning(_( "The Amount of the Voucher can't be zero."))

	@api.multi
	@api.returns('self', lambda value: value.id)
	def copy(self, default=None):
		default = dict(default or {})
		default.update({
			'coupon_code': self._generate_code(),
			'name': ""
			})
		return super(Voucher, self).copy(default)
		
	@api.model
	def _generate_code(self):
		return (hex(random.randrange(111111, 999999)).split('x')[-1].upper())

	@api.model
	def convert_date_format(self, date_type = "start_date"):
		user_date_format = self.env['res.lang']._lang_get(self.env.user.lang).date_format
		return datetime.strftime(self[date_type], user_date_format if user_date_format else '%Y-%m-%d' )

	def convert_amount_format(self, amount):
		cid = self.product_id.currency_id
		fmt = "%.{0}f".format(cid.decimal_places)
		lang = request.env['res.lang']._lang_get(request.env.context.get('lang') or 'en_US')
		res = lang.format(fmt, cid.round(self[amount]), grouping=True, monetary=True)\
			.replace(r' ', u'\N{NO-BREAK SPACE}').replace(r'-', u'-\N{ZERO WIDTH NO-BREAK SPACE}')
		if cid.symbol:
			return '%s %s' % (res, escape(cid.symbol)) if cid.position == 'after' else '%s %s' % (escape(cid.symbol), res)
		return res

	@api.model
	def get_voucher_state (self, offset = 0):

		now = datetime.now().date()

		if not self.active:
			return "inactive"

		if self.is_voucher_limit and self.voucher_limit <= self.applied + offset:
			return "sold_out"

		if self.expiry_date and now > self.expiry_date:
			return "expired"

		if now < self.start_date:
			return "pending"

		return "active"

	@api.multi
	def action_clean (self):
		self.reset_discount()

	@api.model
	def reset_discount(self, orders=False, only_draft=True, delete_order_line=True):

		if not orders:
			orders = self.sale_order_ids

		for order in orders:

			if order.state == "draft" and only_draft:
				order.voucher_code = False
				order.voucher_id = False
				if delete_order_line:
					for i in order.order_line:
						if i.discount_line:
							i.unlink()

	name = fields.Char('Name')
	coupon_code = fields.Char(string="Coupon Code", default=lambda self: self._generate_code())
	product_id = fields.Many2one('product.product','Discount-Product', domain = [('type', '=', 'service'),('is_discount_product', '=', True)])
	active = fields.Boolean('Active',default=True)

	#Value
	amount = fields.Float (string='Coupon Amount')
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
	sale_order_ids = fields.Many2many('sale.order', compute="_compute_voucher")
	applied = fields.Integer('Voucher Count', compute="_compute_voucher")
	applied_display = fields.Char('Applied', compute="_compute_voucher")
	amount_display = fields.Char(string='Amount', compute="_compute_voucher")
	state = fields.Selection([
		("active", "Active"),
		("inactive", "Inactive"),
		("sold_out", "Sold Out"),
		("pending", "Upcoming"),
		("expired", "Expired")
	], default='inactive', compute="_compute_voucher", search='_search_voucher')

	@api.multi
	def _search_voucher(self, operator, value):
		voucher_ids = self.search([]).filtered(lambda x : x.state == value )
		return [('id', operator, [x.id for x in voucher_ids] if voucher_ids else False )]

	@api.model
	@api.depends('is_voucher_limit', 'voucher_limit')
	def _compute_voucher(self):
		
		for voucher in self:
			voucher.applied = request.env['sale.order'].sudo().search_count([('voucher_id', '=', voucher.id)])
			voucher.applied_display = "%s/%s" % (voucher.applied, voucher.voucher_limit if voucher.is_voucher_limit else "∞")
			voucher.state = voucher.get_voucher_state()
			voucher.amount_display = ("%s%s" % (voucher.amount, "%" if voucher.amount_type == "per" else "")) 
			voucher.sale_order_ids = request.env['sale.order'].sudo().search([('voucher_id', '=', voucher.id)])
