from odoo import fields, models, api


class PartnerCreditLimit(models.Model):
    _inherit = 'res.partner'

    blocking_amount = fields.Integer(string='Blocking Amount POS')
