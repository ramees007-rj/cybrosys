from odoo import fields, models


class InheritAccountJournal(models.Model):
    _inherit = 'account.journal'

    credit_check = fields.Boolean(string='Credit')
