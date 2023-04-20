from odoo import fields, models


class InheritHr(models.Model):
    _inherit = 'hr.job'

    minimum_cost = fields.Monetary(string='Hourly Cost')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Currency",
    )


