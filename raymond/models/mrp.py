from odoo import fields, models, api


class MrpInherit(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def create(self, vals_list):
        print(vals_list, "val_list")
        return super().create(vals_list)
