"use strict";

odoo.define('pos_sort_bestseller.models', function (require) {

	var module = require('point_of_sale.models');
	var models = module.PosModel.prototype.models;

	var compare_bestsellers = function(a, b) {
		var comparison = 0;
		if (a.sales_count > b.sales_count) {
			comparison = -1;
		} else if (a.sales_count < b.sales_count) {
			comparison = 1;
		}
		return comparison;
	}

	for(var i=0; i<models.length; i++){
		var model=models[i];
		if(model.model === 'product.product'){
			var old_fnc = model.loaded;
			model.fields.push('sales_count');
			model.loaded = function(self, products) {
				old_fnc(self,products.sort(compare_bestsellers));
			}
		}
	}
});