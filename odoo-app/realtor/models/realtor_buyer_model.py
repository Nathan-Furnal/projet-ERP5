from odoo import fields, models

class Buyer(models.Model):
    _inherit = 'res.partner'
    _description = 'Extension of res.partner'

    offer_ids = fields.One2many('realtor.offer', 'buyer_id', string="Offer")