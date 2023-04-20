from odoo import fields, models


class InheritResCompany(models.Model):
    _inherit = 'res.company'

    bank_details = fields.Text("Bank Details")
