from odoo import fields, models

class Seller(models.Model):
    _inherit = 'res.partner'
    _description = 'Extension of res.partner'

    appart_ids = fields.One2many('realtor.apartment', 'seller_id', string='Seller')