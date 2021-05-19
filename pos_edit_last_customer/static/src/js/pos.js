odoo.define('postags.screen', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var chrome = require('point_of_sale.chrome')
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    

     var ClientEditScreenWidget = screens.ClientListScreenWidget.extend({
        template: 'ClientListScreenWidget',

        show: function (partner_id) {
            var self = this;

            this._super();

            rpc.query({
                model: 'pos.order',
                method: 'search_read',
                domain: [['session_id', '=', self.pos.pos_session.id], ['partner_id', '!=', false]],
                fields: ["partner_id"],
                limit: 1,
                orderBy: [{ name: 'date_order', asc: false }],

            }).then(function (result) {
                if (result.length > 0) {
                    var partner_obj = self.pos.db.get_partner_by_id(result[0].partner_id[0])
                    self.edit_client_details(partner_obj)
                } else {
                    self.gui.back()
                    self.gui.show_popup('error', {
                        'title': _t('Error: Could not Edit Partner'),
                        'body': _t('There is no last customer to edit.'),
                    });
                }
            }, function (err, ev) {
                self.gui.back()
                self.gui.show_popup('error', {
                    'title': _t('Error: Could not Edit Partner'),
                    'body': _t('Your Internet connection is probably down.')
                });

            });
        }
    });

    gui.define_screen({ name: 'editclient', widget: ClientEditScreenWidget });

    var EditLastPartner = PosBaseWidget.extend({
        template: 'EditLastPartner',
        renderElement: function () {
            var self = this;
            this._super();
            this.$el.click(function () {
                self.gui.show_screen('editclient');
            });
        },
    });

    chrome.Chrome.prototype.widgets.splice(2, 0, {
        'name': 'edit_last_partner',
        'widget': EditLastPartner,
        'append': '.pos-rightheader'
    })

});

