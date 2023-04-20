from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    tag = fields.Many2many('estate.property.tag')
    property_type = fields.Many2one("estate.property.type",
                                    string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From", copy=False,
        default=fields.Date.add(fields.Date.today(), months=2))
    Expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price",
                                 readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default='2')
    living_area = fields.Integer(string="Living Area(sqft)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden", )
    garden_area = fields.Integer(string="Garden Area(sqft)")
    garden_orientation = fields.Selection(
        [('south', 'South'), ('north', 'North')],
        string="Garden Orientation")
    property_user = fields.Many2one("res.users", string="Salesman")
    property_partner = fields.Many2one("res.partner", string="Buyer")
    offer_id = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total", string="Total Area",
                                store=True)
    best_offer = fields.Float(compute="_compute_best_offer",
                              string="Best Offer", store=True)
    status = fields.Char(string="Status", default="New", readonly=True)

    def _compute_total(self):
        self.total_area = self.garden_area + self.living_area

    @api.depends("offer_id.price")
    def _compute_best_offer(self):

        self.best_offer = self.offer_id.mapped('price')[-1] if len(
            self.offer_id.mapped('price')) != 0 else 0

        # @api.onchange("garden")
    # def _onchange_garden_orientation(self):
    #     self.garden_orientation = 'north'
    #     self.garden_area = 10

    def sold_item(self):
        if self.status == "Canceled":
            raise UserError('Canceled properties cannot be sold!!!')
        else:
            self.status = "Sold"

    def canceled(self):
        if self.status == "Sold":
            raise UserError('Sold properties cannot be canceled')
        else:
            self.status = "Canceled"
