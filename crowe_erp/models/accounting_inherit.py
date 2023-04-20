from odoo import models, fields, api


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('project.project', string="Project", states={'draft': [('readonly', False)]},
                                 readonly=True, tracking=True)
    task_id = fields.Many2one('project.task', string='Task', states={'draft': [('readonly', False)]}, readonly=True,
                              tracking=True)
    crowe_invoice_type = fields.Selection(
        selection=[('advance', 'Advance'), ('remaining', 'Remaining')])
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='draft',
    )
    invoice_date = fields.Date(
        string='Invoice/Bill Date',
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        copy=False,
        default=fields.Date.today()
    )
    payment_state = fields.Selection(
        selection=[
            ('not_paid', 'Not Paid'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),
            ('reversed', 'Reversed'),
            ('invoicing_legacy', 'Invoicing App Legacy'),
        ],
        string="Payment Status", store=True, readonly=True,
        copy=False,
        tracking=True,
    )


class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    user_id = fields.Many2one('res.users', string='Team Member')
    team_id = fields.Many2one('crm.team', compute='_compute_team_id',
                              store=True)
    task_id = fields.Many2one('project.task')

    @api.depends('user_id')
    def _compute_team_id(self):
        for record in self:
            for rec in self.env['crm.team'].search([]):
                if record.user_id.id in rec.member_ids.mapped('id'):
                    record.team_id = rec.id


class InheritAccountingReport(models.Model):
    _inherit = 'account.invoice.report'

    user_id = fields.Many2one('res.users', string='task user', readonly=True)
    team_id = fields.Many2one('crm.team', string='task team', readonly=True)
    _depends = {
        'account.move.line': ['user_id', 'team_id'],
    }

    def _select(self):
        return super()._select() + ", line.user_id, line.team_id as task_team_id"
