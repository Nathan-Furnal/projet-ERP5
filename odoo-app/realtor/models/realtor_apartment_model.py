from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta

class RealtorApartment(models.Model):
    # Internal name has to be unique
    _name = 'realtor.apartment'
    # Internal description of the apartment
    _description = 'An apartment item inside the realtor application.'

    # Unique name and description
    name = fields.Char(help="Unique apartment name.", required=True)
    description = fields.Char(help="Apartment description.")

    image = fields.Image(help="Image of the appartment.")
    

    # At least 3 months after the creation of the apartment in the module
    available_date = fields.Date(string="Availability date")
    # > 0
    expected_price = fields.Integer(string="Expected price")
    # > 0
    surface_area = fields.Integer(string="Surface area")
    # > 0
    terrace_area = fields.Integer(string="Terrace area")
    # surface_area + terrace_area
    total_area = fields.Integer(string="Total area", compute="_compute_total_area")

    best_amt = fields.Integer(string="Amount of the best offer.")

    buyer_ids = fields.Many2many('res.partner', string='Buyers')

    @api.constrains('best_amt')
    def check_best_amt(self):
        if self.best_amt < int(0.9 * self.expected_price):
            raise exceptions.ValidationError(f"The best offer must be at least 90% of the asking price.")

    @api.constrains('available_date')
    def check_available_date(self):
        if self.available_date < fields.Date.add(fields.Date.today, days=90):
            raise exceptions.ValidationError("The availability date must be at least 3 months past the current date")

    @api.depends('surface_area', 'terrace_area')
    def _compute_total_area(self):
        return self.surface_area + self.terrace_area

    
    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Apartment name must be unique'),
                        ('name_desc_check', 'CHECK(name != description)', 'Name and description must be different'),
                        ('pos_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive.'),
                        ('pos_surface_area', 'CHECK(surface_area > 0)', 'Surface area must be positive.'),
                        ('pos_terrace_area', 'CHECK(terrace_area > 0)', 'Terrace area must be positive.'),
                        ]
