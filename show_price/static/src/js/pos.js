odoo.define('show_price.screen', function (require) {
	"use strict";

	var pos_model = require('point_of_sale.models');
	    pos_model.load_fields("product.product", "standard_price");

});


