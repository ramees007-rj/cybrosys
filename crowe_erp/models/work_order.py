from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class TaskWorkOrder(models.Model):
    _name = 'work.order'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', copy=False, required=True,
                       readonly=True, default=lambda self: _('New'))
    task_id = fields.Many2one('project.task')
    task_state = fields.Selection(related='task_id.state')
    project_id = fields.Many2one('project.project',
                                 string='Project',
                                 related='task_id.project_id', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Name of the Client',
                                 related='task_id.partner_id')
    date_of_commencement = fields.Date(string='Commencement date',
                                       default=fields.Date.today)
    nature_of_work = fields.Text(string='Nature of Work',
                                 related='task_id.sale_line_id.name', readonly=True)
    check_engagement_letter = fields.Boolean(
        string='Engagement Letter Received')
    tentative_date = fields.Date(string='Deadline Date',
                                 related='task_id.date_deadline')
    invoice_percentage = fields.Selection(
        [('0', '0'), ('5', '5'), ('10', '10'), ('15', '15'),
         ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'),
         ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55'),
         ('60', '60'),
         ('65', '65'), ('70', '70'), ('75', '75'), ('80', '80'),
         ('85', '85'), ('90', '90'), ('95', '95'), ('100', '100')],
        string='Invoice Percentage', default='60')
    agreed_amount = fields.Monetary(string='Fee Agreed',
                                    related='task_id.sale_line_id.price_subtotal', readonly=True, store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.company.currency_id,
                                  )
    advance_amount = fields.Float(string='Advance Invoice',
                                  compute='_compute_advance_amount')
    outstanding_amount = fields.Float(string='Outstanding Amount',
                                      readonly=True)
    staff_in_charge_id = fields.Many2one('res.users', string="Staff In-charge",
                                         related='task_id.auditor_id',
                                         readonly=True)

    # Period / year
    current_year_budget = fields.Float(
        string="Current Period Budget (In Hour(s))",
        compute='_compute_current_year_budget',store=True)

    # Audit planning and budget
    constitution = fields.Char(string='Constitution',
                               compute='_compute_audit_planning_budget')
    comm_reg_no = fields.Char(string="Commercial Registration Number")
    members = fields.Char(string='Members')
    accounting_period = fields.Char(string='Accounting Period')
    reg_capital = fields.Char(string="Registered capital (RO)")
    main_activities = fields.Text(string="Main Activities")

    # Client Risk Assessment

    is_inherent = fields.Selection(
        string="Is there any inherent risks to the business ?",
        selection=[('yes', 'YES'), ('no', 'No')])
    is_entity = fields.Selection(
        string="Is the entity, under a direct overview of any regulatory authority ? (SAOG, SAOC, Insurance and brokers, Money exchanges, etc",
        selection=[('yes', 'YES'), ('no', 'No')])
    is_non_availability = fields.Selection(
        string="Non availability of professional management and accounts team ?",
        selection=[('yes', 'Yes'), ('no', 'No')])
    is_proper_account = fields.Selection(
        string="There is no proper accounting system and records ?",
        selection=[('yes', 'YES'), ('no', 'No')])
    is_bank_facilities = fields.Selection(
        string="Is there any bank facilities above RO 2,50,000 , availed by the entity ?",
        selection=[('yes', 'YES'), ('no', 'No'), ])
    is_doubts_entity = fields.Selection(
        string="Doubts entity's ability to continue as a going concern ?",
        selection=[('yes', 'YES'), ('no', 'No')])
    is_significant_estimate = fields.Selection(
        string="Are there any significant estimates and judgement involved ?",
        selection=[('yes', 'YES'), ('no', 'No')])
    is_related_party = fields.Selection(
        string="Are the related party transactions and balances significant ?",
        selection=[('yes', 'YES'), ('no', 'No')])
    is_previous_audit = fields.Selection(
        string="Whether previous year audit report is modified ?",
        selection=[('yes', 'YES'), ('no', 'No')])
    is_fraud_activities = fields.Selection(
        string="Is there any history of fraud activities, non-compliances or branch of laws and regulations ?",
        selection=[('yes', 'YES'), ('no', 'No')])
    risk = fields.Selection(
        string="Based on the above factors, entity's risk is assessed as:",
        selection=[('very_high', 'Very High'), ('high', 'High'),
                   ('medium', 'Medium'),
                   ('low', 'Low')])

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'work.order') or _('New')
        res = super().create(vals)
        return res

    @api.depends('project_id')
    def _compute_audit_planning_budget(self):
        for rec in self:
            rec.write({
                'constitution': self.env['questionnaire'].search(
                    [('partner_id', '=', self.partner_id.id)]).constitution,
                'comm_reg_no': self.env['questionnaire'].search(
                    [('partner_id', '=', self.partner_id.id)]).comm_reg_no,
                'members': self.env['questionnaire'].search(
                    [('partner_id', '=', self.partner_id.id)]).members,
                'reg_capital': self.env['questionnaire'].search(
                    [('partner_id', '=', self.partner_id.id)]).reg_capital,
                'main_activities': self.env['questionnaire'].search(
                    [('partner_id', '=', self.partner_id.id)]).main_activities,
                'accounting_period': self.env['questionnaire'].search([(
                    'partner_id',
                    '=',
                    self.partner_id.id)]).accounting_period
            })

    @api.depends('project_id')
    def _compute_current_year_budget(self):
        for rec in self:
            rec.write({
                'current_year_budget': sum(
                    rec.project_id.cost_sheet_id.cost_sheet_line_ids.search(
                        [('cost_sheet_id', '=',
                          rec.project_id.cost_sheet_id.id),
                         ('product_id', '=',
                          rec.task_id.sale_line_id.product_id.id)]).mapped(
                        'man_hours'))
            })

    def action_print(self):
        data = {
            'dd': 'dd'
        }
        return self.env.ref(
            'crowe_erp.action_report_work_order').report_action(self,
                                                                data=data)

    @api.depends('invoice_percentage')
    def _compute_advance_amount(self):
        for rec in self:
            advance_amount = (rec.agreed_amount * int(
                rec.invoice_percentage)) / 100
            rec.write({
                'advance_amount': advance_amount,
                'outstanding_amount': rec.agreed_amount - advance_amount
            })

    @api.onchange('current_year_budget')
    def _onchange_current_year_budget(self):
        self.task_id.write({
            'planned_hours': self.current_year_budget,
        })

    def action_approve(self):
        # if self.project_id.sale_order_id.partner_id.credit > 0:
        #     raise ValidationError(
        #         "You can't proceed the work order,Customer has credit.")
        # else:
        if self.invoice_percentage:
            if self.project_id.invoice_type == 'combine':
                if self.env['project.task'].search_count(
                        [('project_id', '=', self.project_id.id)]) != self.env[
                    'work.order'].search_count(
                    [('project_id', '=', self.project_id.id)]):
                    raise ValidationError("Create WorkOrders for all tasks")
                else:
                    line_ids = []
                    for rec in self.env['work.order'].search(
                            [('project_id', '=', self.project_id.id)]):
                        line_ids.append((0, 0, {
                            'task_id': rec.task_id.id,
                            'wo_id': rec.id,
                            'amount': (rec.agreed_amount * int(
                                rec.invoice_percentage)) / 100}))
                    return {
                        'type': 'ir.actions.act_window',
                        'name': self.invoice_percentage + '% advance billing for ' + self.nature_of_work,
                        'view_mode': 'form',
                        'res_model': 'advance.invoice.wo',
                        'target': 'new',
                        'context': {
                            'default_task_id': self.task_id.id,
                            'default_work_order_id': line_ids
                        }
                    }
            elif self.project_id.invoice_type == 'individual':
                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': self.project_id.sale_order_id.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'project_id': self.project_id.id,
                    'task_id': self.task_id.id,
                    'crowe_invoice_type': 'advance',
                    'invoice_line_ids': [(0, 0, {
                        'product_id': self.task_id.sale_line_id.product_id.id,
                        'name': self.invoice_percentage + '% advance billing for ' + self.nature_of_work,
                        'company_id': self.env.company.id,
                        'user_id': self.task_id.auditor_id.id,
                        'price_unit': (self.agreed_amount * int(
                            self.invoice_percentage)) / 100
                    })]
                })
                self.task_id.sale_line_id.write({
                    'invoice_lines': [(4, invoice.invoice_line_ids.id)]
                })
                self.task_id.write({
                    'invoice_amount': (self.agreed_amount * int(
                        self.invoice_percentage)) / 100
                })

            # state changing
            if self.task_id.sale_line_id.product_id.categ_id.id == self.env.ref(
                    'crowe_erp.product_category_task_type_short').id:
                self.task_id.write({
                    'wo_approved_user_id': self.env.user.id,
                    'Wo_approved_time': fields.Datetime.now(),
                    'state': 'engagement_partner',
                    'task_flow_type': 'short'
                })
            elif self.task_id.sale_line_id.product_id.categ_id.id == self.env.ref(
                    'crowe_erp.product_category_task_type_medium').id:
                self.task_id.write({
                    'wo_approved_user_id': self.env.user.id,
                    'Wo_approved_time': fields.Datetime.now(),
                    'state': 'wo_completed',
                    'task_flow_type': 'medium'
                })
            else:
                self.task_id.write({
                    'wo_approved_user_id': self.env.user.id,
                    'Wo_approved_time': fields.Datetime.now(),
                    'state': 'wo_completed'
                })


class AdvanceInvoiceWO(models.TransientModel):
    _name = 'advance.invoice.wo'

    task_id = fields.Many2one('project.task')
    project_id = fields.Many2one('project.project',
                                 related='task_id.project_id',
                                 string='Project',
                                 readonly=True)
    work_order_id = fields.One2many('advance.invoice.wo.line', 'work_order_id',
                                    string='Work Order', readonly=True)

    def action_create_invoice(self):
        line_ids = []
        for rec in self.work_order_id:
            line_ids.append((0, 0, {
                'product_id': rec.task_id.sale_line_id.product_id.id,
                'name': rec.wo_id.invoice_percentage + '% advance billing for ' + rec.wo_id.nature_of_work,
                'company_id': rec.env.company.id,
                'price_unit': rec.amount,
                'user_id': rec.task_id.auditor_id.id,
                'task_id': rec.task_id.id
            }))
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.project_id.sale_order_id.partner_id.id,
            'invoice_date': fields.Date.today(),
            'project_id':self.project_id.id,
            'crowe_invoice_type': 'advance',
            'invoice_line_ids': line_ids
        })
        invoice_line_ids = []
        for rec in invoice.invoice_line_ids:
            invoice_line_ids.append((4, rec.id))
            rec.task_id.write({
                'invoice_amount': rec.price_unit
            })
            if rec.task_id.sale_line_id.product_id.categ_id.id == rec.env.ref(
                    'crowe_erp.product_category_task_type_short').id:
                rec.task_id.write({
                    'wo_approved_user_id': self.env.user.id,
                    'Wo_approved_time': fields.Datetime.now(),
                    'state': 'engagement_partner',
                    'task_flow_type': 'short'
                })
            elif rec.task_id.sale_line_id.product_id.categ_id.id == rec.env.ref(
                    'crowe_erp.product_category_task_type_medium').id:
                rec.task_id.write({
                    'wo_approved_user_id': self.env.user.id,
                    'Wo_approved_time': fields.Datetime.now(),
                    'state': 'wo_completed',
                    'task_flow_type': 'medium'
                })
            else:
                rec.task_id.write({
                    'wo_approved_user_id': self.env.user.id,
                    'Wo_approved_time': fields.Datetime.now(),
                    'state': 'wo_completed'
                })
        self.task_id.sale_line_id.write({
            'invoice_lines': invoice_line_ids
        })


class AdvanceInvoiceWO(models.TransientModel):
    _name = 'advance.invoice.wo.line'

    work_order_id = fields.Many2one('advance.invoice.wo.line')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    wo_id = fields.Many2one('work.order', string='Work Order')
    amount = fields.Float('Amount')
