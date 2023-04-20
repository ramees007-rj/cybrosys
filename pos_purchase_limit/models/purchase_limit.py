from odoo import models, fields


class PurchaseLimit(models.Model):
    _inherit = 'res.partner'

    active_purchase_limit = fields.Boolean(string='Purchase Limit')
    purchase_limit = fields.Integer()
