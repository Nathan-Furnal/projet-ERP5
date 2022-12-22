from odoo import models, fields, api

class RealtorProduct(models.Model):
    _inherit = 'product.template'

    apart_id = fields.Many2one("realtor.apartment", string="Property", ondelete='cascade')

    list_price = fields.Float(compute='_update_prod_price')

    @api.onchange('apart_id')
    def _update_prod_price(self):
        for el in self:
            el.list_price = el.apart_id.expected_price