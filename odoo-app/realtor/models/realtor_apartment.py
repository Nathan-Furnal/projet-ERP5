from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import ValidationError

class RealtorApartment(models.Model):
    _name = 'realtor.apartment'
    _description = 'An apartement unit'

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_best_price", "CHECK(best_price >= 0)", "The best offer price must be positive"),
        ("check_apart_area", "CHECK(apartment_area > 0)", "The apartment area must be strictly positive"),
    ]

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)    

    name = fields.Char("Title", required=True)
    desc = fields.Text("Description")

    img = fields.Image()

    availability_date = fields.Date("Available from", default=lambda self: self._default_date_availability(), copy=False)

    expected_price = fields.Float("Expected Price", required=True)
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    apartment_area = fields.Integer("Apartment area")
    terrace_area = fields.Integer("Terrace Area")

    total_area = fields.Integer("Total area", compute='_compute_total_area')

    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    offer_ids = fields.One2many("realtor.offer", "property_id", string="Offers")

    @api.depends('apartment_area', 'terrace_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.apartment_area + prop.terrace_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0            


    @api.constrains("expected_price", "best_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.best_price, precision_rounding=0.01)
                and float_compare(prop.best_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )