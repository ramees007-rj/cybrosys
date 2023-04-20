from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].append('credit')
        result['search_params']['fields'].append('use_partner_credit_limit')
        result['search_params']['fields'].append('credit_limit')
        result['search_params']['fields'].append('blocking_amount')
        return result
