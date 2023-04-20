from odoo import models, fields


class CustomerMo(models.Model):
    _name = 'mrp.production'
    _inherit = ['mrp.production', 'portal.mixin']

    customer_id = fields.Many2one('res.partner')

    def _compute_access_url(self):
        super(CustomerMo, self)._compute_access_url()
        for mo in self:
            mo.access_url = '/my/mo/%s' % (mo.id)
