from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

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

    img = fields.Image("Apartment's picture")

    availability_date = fields.Date("Available from", default=lambda self: self._default_date_availability(), copy=False)

    expected_price = fields.Float("Expected Price", required=True)
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)

    apartment_area = fields.Integer("Apartment area")
    terrace_area = fields.Integer("Terrace Area")

    total_area = fields.Integer("Total area", compute='_compute_total_area')

    # Special   
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean("Active", default=True)

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
                    "The BEST price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The SELLING price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )   

    # ------------------------------------------ CRUD Methods -------------------------------------

    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")
        return super().unlink()

    # ---------------------------------------- Action Methods -------------------------------------

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})             