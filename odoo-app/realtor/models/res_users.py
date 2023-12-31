# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.users"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Relational
    
    property_ids = fields.One2many(
        "realtor.apartment", "user_id", string="Properties")