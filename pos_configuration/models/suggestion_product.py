from odoo import fields, models, api


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'

    suggestion_product_ids = fields.Many2many('product.product',
                                              'suggestion_product_rel',
                                              string='Suggestion Product')

