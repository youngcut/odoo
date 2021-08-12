# -*- coding: utf-8 -*-
from odoo import fields
from odoo.http import request
from odoo.tools.translate import _
import odoo.http as http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebVoucher(WebsiteSale):

	@http.route(['/shop/voucher'], type='json', auth="public", website=True, sitemap=False)
	def add_voucher_json(self, code='', **post):

		order = request.website.sale_get_order()
		order.voucher_code = code
		order.voucher_id = request.env['voucher'].with_context(active_test=False).sudo().search([('coupon_code','=', code)])
		order.check_discount()
		return {
			'website_sale.cart_lines': request.env['ir.ui.view'].render_template("website_sale.cart_lines", {
				'website_sale_order': order,
				'date': fields.Date.today(),
				'suggested_products': order._cart_accessories()
			}),
			'website_sale.short_cart_summary': request.env['ir.ui.view'].render_template("website_sale.short_cart_summary", {
				'website_sale_order': order,
			}),
			'voucher': order.check_discount(),
		}
		
	@http.route(['/shop/voucher/<string:code>'], type='http',auth="public",  methods=["GET"], website=True, sitemap=False)
	def add_voucher(self, code='', **kw):

		order = request.website.sale_get_order(force_create=1)
		order.voucher_code = code
		order.voucher_id = request.env['voucher'].with_context(active_test=False).sudo().search([('coupon_code','=', code)])
		order.check_discount()
		return request.redirect('/shop/cart')

