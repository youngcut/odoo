odoo.define('show_daily_earnings.screen', function (require) {
	"use strict";

	var screens = require('point_of_sale.screens');
	var chrome = require('point_of_sale.chrome')
	var PosBaseWidget = require('point_of_sale.BaseWidget');
	var rpc = require('web.rpc');

	var set_daily_earnings = function() {
		rpc.query({
			model: 'report.point_of_sale.report_saledetails',
			method: 'get_sale_details'
		}).then(function(result) {
			$('.daily_earning').html(result.total_paid.toFixed(2));
		});
	}

	chrome.Chrome.prototype.widgets.splice(1, 0, {
		'name':   'daily_earnings',
		'widget': PosBaseWidget.extend({template: 'DailyEarnings'}),
		'append':  '.pos-rightheader'
	})

	screens.PaymentScreenWidget.include({
		order_changes: function () {
			this._super.apply(this, arguments);
			set_daily_earnings();
		},
		init: function () {
			this._super.apply(this, arguments);
			set_daily_earnings();
		}
	});

});


