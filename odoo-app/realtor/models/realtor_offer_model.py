from odoo import fields, models

class RealtorOffer(models.Model):
    _name = 'realtor.offer'
    _description = 'An offer placed on an apartment'

    name = fields.Char()
    amt = fields.Integer(help="Amount offered")

    buyer_id = fields.Many2one('res.partner', 'offer_id')

    _sql_constraints = [('pos_amt', 'CHECK(amt > 0)', 'The amount of the offer must be positive')]