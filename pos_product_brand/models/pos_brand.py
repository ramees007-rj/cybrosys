from odoo import models, fields


class PosBrand(models.Model):
    _inherit = "product.template"

    brand_name = fields.Char(string='Brand')
