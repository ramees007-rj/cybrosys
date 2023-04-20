from odoo import models


class InheritPaySlip(models.Model):
    _name = 'hr.payslip'
    _inherit = ['hr.payslip', 'portal.mixin']

    def _compute_access_url(self):
        super(InheritPaySlip, self)._compute_access_url()
        for p in self:
            p.access_url = '/my/payslip/%s' % (p.id)