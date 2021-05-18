odoo.define('greeninca.screen', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var field_utils = require('web.field_utils');

    screens.ClientListScreenWidget.include({

        display_client_details: function (visibility, partner, clickpos) {

            var _super_fnc = this._super.bind(this);

            if (visibility == "show") {
                rpc.query({
                    model: 'res.partner',
                    method: 'get_sales_of_partner',
                    kwargs: {partner: partner.id}
                })
                .then(function (partner_sales) {

                    partner.sales = partner_sales.map(function(a) {
                        a.date = field_utils.format.date(moment(a.date), {}, { timezone: false });
                        return a
                    })

                    _super_fnc(visibility, partner, clickpos);

                })

            } else {
                _super_fnc(visibility, partner, clickpos);
            }

        }


    });

});

