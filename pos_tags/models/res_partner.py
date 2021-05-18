# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    @api.model
    def get_tagnames_of_partner (self, partner = 0):

        return list(map(lambda x: {
            'value': x.id,
            'text': x.name,
            'assign': partner in x.partner_ids.ids
        } , self.env['res.partner.category'].sudo().search([('active', '=', True)])))

class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def create_from_ui(self, partner):
        partner_id = super(ResPartner, self).create_from_ui(partner)

        self.browse(partner_id).write({'category_id': [(6, 0, [int(x) for x in partner['category_id'].split(',')])]})

        return partner_id