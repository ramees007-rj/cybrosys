from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'property_type'

    name = fields.Char(string="Name", required=True)


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'property_tag'

    name = fields.Char(string="name", required=True)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate_offer'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'),
                               ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property")
    date_deadline = fields.Date(
        compute="_compute_dead_line",
        inverse="_inverse_validity", string="Dead line", store=True)
    validity = fields.Integer(default=7, string="Validity(days)")

    @api.depends('validity')
    def _compute_dead_line(self):
        self.date_deadline = fields.Date.add(fields.Date.today(),
                                             days=self.validity)

    def _inverse_validity(self):
        self.validity = int(self.date_deadline.strftime("%j")) - int(
            fields.Date.today().strftime("%j"))

    def validate(self):
        self.status = 'accepted'
        self.property_id.property_partner = self.partner_id
        self.property_id.selling_price = self.price

        return True

