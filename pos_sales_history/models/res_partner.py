# -*- coding: utf-8 -*-
from odoo import api, fields, models

class GreenIncaResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_sales_of_partner(self, partner):
        
        output = []

        for pos_sale in self.env['pos.order'].search([('partner_id', '=', partner)]):
            for items in self.env['pos.order.line'].search([('order_id', '=', pos_sale.id)]):
                output.append({
                    'id': items.id,
                    'name': items.product_id.name,
                    'date': items.create_date,
                    'origin': "POS",
                    'qty': items.qty,
                    'price': items.price_subtotal_incl
                })

        for sale_order_line in self.env['sale.order.line'].search([('order_partner_id', '=', partner), ("product_id.type", "=", "product")]):
            output.append({
                'id': sale_order_line.id,
                'name': sale_order_line.name,
                'date': sale_order_line.create_date,
                'qty': sale_order_line.product_uom_qty,
                'origin': "Online",
                'price': sale_order_line.price_total
            })

        return sorted(output, key=lambda x: x['date'], reverse=True)
