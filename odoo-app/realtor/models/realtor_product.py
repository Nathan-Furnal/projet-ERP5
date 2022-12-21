from odoo import models, fields

class RealtorProduct(models.Model):
    _inherit = 'product.template'

    # apart_ids = fields.One2many("realtor.apartment", 'product_id', string="Properties")