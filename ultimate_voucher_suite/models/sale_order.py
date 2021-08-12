# -*- coding: utf-8 -*-

import uuid
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.http import request
from datetime import datetime

@api.multi
class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.model
	def action_done(self):
		return super(SaleOrder, self).action_done()

	@api.multi
	def action_cancel(self):
		return super(SaleOrder, self).action_cancel()

	@api.multi
	def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):

		#Customer removed the voucher
		if (product_id == int(self.voucher_id.product_id.id)):
			self.voucher_id.reset_discount([self])

		#Do cart update
		old_cart_update = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)

		self.check_discount()

		return old_cart_update

	voucher_id = fields.Many2one("voucher", string="Voucher")
	voucher_code = fields.Char("Voucher Code")
	voucher_discount = fields.Monetary("Discount-Value")
	
	@api.depends('voucher_code', 'voucher_id', 'voucher_discount', 'state', 'partner_id')
	def _get_voucher_state (self):

		self.ensure_one()

		if not self.voucher_code:
			return ("not_set", _("Have a Voucher code? Fill in this field and apply."), "info")
		
		if not self.voucher_id:
			return ("invalid", _("Invalid Voucher Code! Try again:"), "danger")

		if self.state == "draft":

			voucher_state = self.voucher_id.get_voucher_state(-1)

			if voucher_state == "inactive":
				return ("inactive", _("Voucher is not active."), "danger")

			if voucher_state == "sold_out":
				return ("sold_out", _("The quantum of this coupon code is already used up!"), "danger")

			if voucher_state == "pending":
				return ("pending", _("The voucher will be valid soon! Try on %s again.") % self.voucher_id.convert_date_format(), "danger")

			if voucher_state == "expired":
				return ("expired", _("This coupon code has already expired!"), "danger")

			if self.voucher_id.partner_id and not (self.partner_id in self.voucher_id.partner_id):
				return ("wrong_partner", _("This voucher is intended for another customer. Login and try again."), "danger")
			
			#calculate discount_value
			self.voucher_discount = 0
			for product in self.order_line:
				if not self.voucher_id.product_valid or (self.voucher_id.product_valid and product.product_id in self.voucher_id.product_valid):
					self.voucher_discount += product.price_total if self.voucher_id.amount_type == 'fix' else ((product.price_total * self.voucher_id.amount)/100)

			if self.voucher_id.product_valid and self.voucher_discount == 0:
				return ("restrict", _("This code is only valid for the following products:"), "warning")

			if self.voucher_id.min_amount and (self.voucher_discount < self.voucher_id.min_amount):
				self.voucher_discount = 0
				return ("min_not_reached", _("The discount will be added as soon as you reach the minimum amount of %s.") % self.voucher_id.convert_amount_format("min_amount"), "warning")

			if self.voucher_discount > self.voucher_id.amount:
				self.voucher_discount = self.voucher_id.amount

			if self.voucher_id.max_amount and self.voucher_id.amount_type == 'per' and self.voucher_discount > self.voucher_id.max_amount:
				return ("max_reached", _("The maximum voucher value has been reached."), "warning")

			if self.voucher_id.amount_type == 'fix' and self.voucher_discount < self.voucher_id.amount:
				return ("not_reached", _("The voucher value (%s) has not yet been reached. You can add more items to cart!") % self.voucher_id.convert_amount_format("amount"), "success")

		return ("applied", _("The Discount '%s' is added to your cart !") % self.voucher_id.name, "success")


	@api.multi
	def check_discount(self):
		self.ensure_one()
		if self.state == "draft":

			for i in self.order_line:
				if i.discount_line:
					i.unlink()

			vstate = self._get_voucher_state()

			# No or not critical errors: Keep voucher
			if vstate[2] in ["success","warning"]:
				discount_line = request.env['sale.order.line'].sudo().search([]).sudo().create({
					'product_id': int(self.voucher_id.product_id.id),
					'name': self.voucher_id.product_id.name,
					'price_unit': -self.voucher_discount,
					'order_id': self.id,
					'product_uom':self.voucher_id.product_id.uom_id.id,
					'discount_line':True
				})
							
		return {
			'state': vstate[0],
			'message': vstate[1],
			'type': vstate[2]
		}
	


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	discount_line = fields.Boolean(string='Discount line',readonly=True)

class ProductTemplate(models.Model):
	_inherit = 'product.template'
	is_discount_product = fields.Boolean(string='Voucher Product')