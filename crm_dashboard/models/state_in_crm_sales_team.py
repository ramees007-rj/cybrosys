from odoo import models, fields, api
from datetime import datetime


class InheritCrmTeam(models.Model):
    _inherit = 'crm.team'

    crm_state = fields.Many2one('crm.stage', string='State')


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        res = super(InheritSaleOrder, self)._action_confirm()
        self.opportunity_id.stage_id = self.team_id.crm_state
        return res


class InheritCrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def check_user_group(self):
        user = self.env.user
        ss = datetime.today().year, 1, 1
        dd = datetime.today().year, 12, 31
        mm1 = datetime.today().replace(day=1)
        print(self.env['crm.lead'].search_read(
            [('date_deadline', '>', ss), ('date_deadline', '<', dd)], limit=1))
        if user.has_group('sales_team.group_sale_manager'):
            return True
        else:
            return False

    @api.model
    def check_dashboard_values(self, date, com_id):
        # print(type("dsdddddddddddddddddddd",date['key1']))
        user = self.env.user
        if user.has_group('sales_team.group_sale_manager'):
            lead_count = self.env['crm.lead'].search_count(
                [('create_date', '>', date['key1']),
                 ('create_date', '<', date['key2'])])
            opportunity_count = self.env['crm.lead'].search_count(
                [('create_date', '>', date['key1']),
                 ('create_date', '<', date['key2']),
                 ('type', '=', 'opportunity')])
            expected_revenue = sum(
                self.env['crm.lead'].search(
                    [('create_date', '>', date['key1']),
                     ('create_date', '<', date['key2'])]).mapped(
                    'expected_revenue'))
            revenue = sum(self.env['account.move'].search(
                [('invoice_date', '>', date['key1']),
                 ('invoice_date', '<', date['key2'])]).mapped('amount_total'))
            lost_amount = sum(self.env['crm.lead'].search(
                [('probability', '=', 0), ('active', '=', False),
                 ('create_date', '>', date['key1']),
                 ('create_date', '<', date['key2'])]).mapped(
                'expected_revenue'))
            win_amount = sum(self.env['crm.lead'].search(
                [('active', '=', True),
                 ('stage_id.is_won', '=', True),('create_date', '>', date['key1']),('create_date', '<', date['key2'])]).mapped(
                'expected_revenue'))
            currency = self.env['res.company'].browse(
                com_id).currency_id.symbol
            val = {
                'lead_count': lead_count,
                'opportunity_count': opportunity_count,
                'expected_revenue': expected_revenue,
                'revenue': revenue,
                'won_amount': win_amount,
                'lost_amount': lost_amount,
                'currency': currency,
            }
            return val
        else:
            lead_count = self.env['crm.lead'].search_count(
                [('user_id', '=', user.id), ('create_date', '>', date['key1']),
                 ('create_date', '<', date['key2'])])
            opportunity_count = self.env['crm.lead'].search_count(
                [('user_id', '=', user.id), ('create_date', '>', date['key1']),
                 ('create_date', '<', date['key2']),
                 ('type', '=', 'opportunity')])
            expected_revenue = sum(
                self.env['crm.lead'].search(
                    [('create_date', '>', date['key1']),
                     ('create_date', '<', date['key2'])]).mapped(
                    'expected_revenue'))
            revenue = sum(self.env['account.move'].search(
                [('user_id', '=', user.id),
                 ('invoice_date', '>', date['key1']),
                 ('invoice_date', '<', date['key2'])]).mapped('amount_total'))
            win_amount = sum(self.env['crm.lead'].search(
                [('user_id', '=', user.id), ('probability', '=', 0),
                 ('active', '=', False),
                 ('create_date', '>', date['key1']),
                 ('create_date', '<', date['key2'])]).mapped(
                'expected_revenue'))
            lost_amount = sum(self.env['crm.lead'].search(
                [('user_id', '=', user.id), ('active', '=', True),
                 ('stage_id.is_won', '=', True),
                 ('create_date', '>', date['key1']),
                 ('create_date', '<', date['key2'])]).mapped(
                'expected_revenue'))
            currency = self.env['res.company'].browse(
                com_id).currency_id.symbol
            val = {
                'lead_count': lead_count,
                'opportunity_count': opportunity_count,
                'expected_revenue': expected_revenue,
                'revenue': revenue,
                'win_amount': win_amount,
                'lost_amount': lost_amount,
                'currency': currency,
            }
            return val
