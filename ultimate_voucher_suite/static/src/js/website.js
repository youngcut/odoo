
odoo.define('odoo_website_discount_voucher.odoo_website_voucher', function(require) {
	"use strict";

	var sAnimations = require('website.content.snippets.animation');

	sAnimations.registry.Voucher = sAnimations.Class.extend({
		selector: '.oe_website_sale',
		read_events: {
			'click button.js_add_voucher_json': '_onClickAddVoucher',
			'keypress input.js_code_voucher_json': '_onKeyPressVoucher'

		},

		/**
		 * @constructor
		 */
		init: function () {
			this._super.apply(this, arguments);
			this._releaseWait()

		},
		/**
		 * @private
		 */
		_validVoucher: function ($code) {

			var _this = this;

			this._rpc({
				route: "/shop/voucher",
				params: {
					code: $code
				},
			}).then(function (data) {

				$(".js_cart_lines").first().before(data['website_sale.cart_lines']).end().remove();
				$(".js_cart_summary").first().before(data['website_sale.short_cart_summary']).end().remove();

				_this._releaseWait()
				
				
			});
		},

		/**
		 * @private
		 */
		_releaseWait() {
			var $wait_btn = $('.wait');
			var $wait_text = $wait_btn.data('loading-text');
			if ($wait_btn.length > 0) {
				var count = 5
				$wait_btn.html($wait_text.replace('%s', count))
				var timer = setInterval(function () {
					count--
					$wait_btn.html($wait_text.replace('%s', count))
					if (count === 0) {
						$wait_btn.html("Apply").removeAttr('disabled')
						clearInterval(timer)
					}
				}, 1000)

			}
		},

		/**
		 * @private
		 * @param {Event} ev
		 */
		 _onClickAddVoucher: function (ev) {

			var $btn = $(ev.currentTarget)
			$btn.append('&nbsp;<span class="fa fa-cog fa-spin"/>');
			$btn.attr('disabled', 'disabled')
			this._validVoucher($btn.prev('input').val());
		},
		/**
		 * @private
		 * @param {Event} ev
		 */
		 _onKeyPressVoucher: function (ev) {

			 var $btn = $(ev.currentTarget).next('button')

			 if (ev.keyCode === 13 && !$btn.attr('disabled')) {
				 // Cancel the default action, if needed
				 ev.preventDefault();
				 // Trigger the button element with a click
				 this._onClickAddVoucher({'currentTarget': $btn})
			 }
		}
		
	});

});

