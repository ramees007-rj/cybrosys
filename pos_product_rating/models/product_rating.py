from odoo import models, fields


class Rating(models.Model):
    _inherit = "product.template"

    product_quality = fields.Selection([('1', '1'),
                                        ('2', '2'),
                                        ('3', '3'),
                                        ('4', '4'),
                                        ('5', '5')],
                                       string='Product Quality', default='1')
