from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class InheritProjectTask(models.Model):
    _inherit = 'project.task'

    invoice_amount = fields.Float(string='invoiced amount', default=0)
    planned_hours = fields.Float("Initially Planned Hours", tracking=True,
                                 readonly=True)
    full_invoice_check = fields.Boolean()
    project_director_id = fields.Many2one('res.users',
                                          related='project_id.user_id',
                                          readonly=False,
                                          string='Project Director',
                                          store=True)
    supervisor_id = fields.Many2one('res.users', string="Supervisor")
    case_ware_check = fields.Boolean(string='Caseware completed')
    reviewed_id = fields.Many2one('res.users', string="Reviewer")
    comment_id = fields.Many2one('res.users', string="Comments Addressed By")
    engagement_partner_id = fields.Many2one('res.users',
                                            string="Engagement Partner")
    engagement_comments_id = fields.Many2one('res.users',
                                             string="Engagement Comments Addressed By")
    auditor_id = fields.Many2one('res.users', related='project_id.user_id',
                                 string='Staff in Charge', readonly=False)

    # Preliminary clearance
    letter_of_rep_check = fields.Boolean(string='Letter of representation')
    letter_of_engagement_next_year_check = fields.Boolean(
        string='Letter of engagement for the next year')
    draft_deliverables_check = fields.Boolean(string='Draft Deliverables')
    management_letter_check = fields.Boolean(string='Management Letter')
    draft_check_user_id = fields.Many2one('res.users', string='Draft Issued')
    draft_compared_user_id = fields.Many2one('res.users',
                                             string='Draft Compared By')
    draft_checked_user_id = fields.Many2one('res.users',
                                            string='Draft Checked BY')
    task_flow_type = fields.Char()

    # Managing Partner Review
    has_need_quality_check = fields.Boolean(string='Needs Quality Review')
    quality_reviewer_id = fields.Many2one('res.users',
                                          string="Quality Reviewer")
    open_items_req = fields.Text(
        string="Open items requiring hold on release of report")

    # Final Clearance details

    letter_of_rep_check_head = fields.Boolean(
        "Letter of representation duly signed and stamped on client’s letter head")
    draft_duly_check = fields.Boolean(
        "Draft duly stamped and signed on all pages.")
    eng_letter_check = fields.Boolean(
        "Letter of engagement for the next year duly signed")
    final_tbalance_check = fields.Boolean("Final Trial balance.")
    pending_check = fields.Boolean("All pending documents cleared.")
    compared_agreed_check = fields.Boolean("Compared and agreed to draft FSs")

    # Engagement Partner Signed Off
    final_clearance_aud_partner_id = fields.Many2one("res.users",
                                                     string="Engagement Partner")
    checked_id = fields.Many2one("res.users", string="Final Checked By")
    checked_date = fields.Datetime(string="Checked Date", readonly=True)
    issued_by = fields.Many2one("res.users", string="Final Issued By")
    issued_by_date = fields.Datetime(string="Issued By Date", readonly=True)

    # Managing Partner Sign Off
    manager_partner_id = fields.Many2one("res.users", string="Manager Partner")
    # Meeting
    meeting_type = fields.Selection(
        [('board', 'Board'), ('agm', 'AGM'), ('ac', 'AC'), ('none', 'None')],
        string='Meeting', default='none')
    meeting_date = fields.Date(string='Meeting Date')

    # Sign off details
    allocated_user_id = fields.Many2one('res.users', string='Allocated', readonly=True)
    allocated_time = fields.Datetime("allocated_time", readonly=True)
    wo_approved_user_id = fields.Many2one('res.users',
                                          string='Work Order Approved', readonly=True)
    Wo_approved_time = fields.Datetime("Wo_approved_time", readonly=True)
    field_work_started_user_id = fields.Many2one('res.users',
                                                 string='Field Work Started', readonly=True)
    field_work_started_time = fields.Datetime("field_work_started_time", readonly=True)
    field_work_complete_user_id = fields.Many2one('res.users',
                                                  string='Field Work Completed', readonly=True)
    fo_completed_time = fields.Datetime("fo_completed_time", readonly=True)
    supervisor_user_id = fields.Many2one('res.users', string='Supervisor User', readonly=True)
    supervisor_time = fields.Datetime("supervisor_time", readonly=True)
    manager_review_user_id = fields.Many2one('res.users',
                                             string='Manager Review', readonly=True)
    manager_date = fields.Datetime("manager_date", readonly=True)
    ep_review_user_id = fields.Many2one('res.users',
                                        string='Engagement Partner Review', readonly=True)
    ep_review_time = fields.Datetime("ep_review_time", readonly=True)
    preliminary_clearance_user_id = fields.Many2one('res.users',
                                                    string='Preliminary Clearance', readonly=True)
    preliminary_clearance_time = fields.Datetime("preliminary_clearance_time", readonly=True)
    draft_dele_user_id = fields.Many2one('res.users',
                                         string='Draft Deliverable', readonly=True)
    draft_dele_time = fields.Datetime("draft_dele_time", readonly=True)
    final_clearance_user_id = fields.Many2one('res.users',
                                              string='Financial Clearance', readonly=True)
    final_clearance_time = fields.Datetime("final_clearance_time", readonly=True)
    ep_sign_off_user_id = fields.Many2one('res.users',
                                          string='Engagement Partner Sign Off', readonly=True)
    ep_sign_off_time = fields.Datetime("ep_sign_off_time", readonly=True)
    final_delivered_user_id = fields.Many2one('res.users',
                                              string='Financial Delivered', readonly=True)
    final_delivered_time = fields.Datetime("final_delivered_time", readonly=True)
    complete_user_id = fields.Many2one('res.users', string='Completion', readonly=True)
    complete_time = fields.Datetime("complete_time", readonly=True)

    state = fields.Selection([
        ('new', 'New'),
        ('allocated', 'Allocated'),
        ('wo_completed', 'Work Order Approved'),
        ('field_work_started', 'Field Work Started'),
        ('field_work_completed', 'Field Work Completed'),
        ('supervisor_sign_off', 'Supervisor Check'),
        ('reviewer_sign_off', 'Manager Review'),
        ('engagement_partner', 'Engagement Partner Review'),
        ('preliminary_clearance', 'Preliminary clearance'),
        ('draft_report_delivered', 'Draft Delivered'),
        ('final_clearance', 'Final Clearance'),
        ('audit_partner_sign_off', 'Engagement Partner Sign Off'),
        ('deliver_final_report', 'Final Delivered'),
        ('complete', 'Complete')
    ], string='State', default='new', tracking=True)

    @api.onchange('checked_id')
    def _onchange_checked_id(self):
        self.write({
            'checked_date': fields.Datetime.now()
        })

    @api.onchange('issued_by')
    def _onchange_issued_by(self):
        self.write({
            'issued_by_date': fields.Datetime.now()
        })

    def action_allocate(self):
        if self.auditor_id:
            self.write({
                'allocated_user_id': self.env.user.id,
                'allocated_time': fields.Datetime.now(),
                'state': 'allocated',
                'user_ids': [(4, self.auditor_id.id)]
            })
        else:
            raise ValidationError("Please choose a auditor")

    def action_print_rcs(self):
        data = {
            'allocated': self.allocated_user_id.name if self.allocated_user_id else None,
            'allocated_time': self.allocated_time if self.allocated_time else None,
            'wo_approved_user_id': self.wo_approved_user_id.name if self.wo_approved_user_id else None,
            'Wo_approved_time': self.Wo_approved_time if self.Wo_approved_time else None,
            'field_work_started_user_id': self.field_work_started_user_id.name if self.field_work_started_user_id else None,
            'field_work_started_time': self.field_work_started_time if self.field_work_started_time else None,
            'field_work_complete_user_id': self.field_work_complete_user_id.name if self.field_work_complete_user_id else None,
            'fo_completed_time': self.fo_completed_time if self.fo_completed_time else None,
            'supervisor_user_id': self.supervisor_user_id.name if self.supervisor_user_id else None,
            'supervisor_time': self.supervisor_time if self.supervisor_time else None,
            'manager_review_user_id': self.manager_review_user_id.name if self.manager_review_user_id else None,
            'manager_date': self.manager_date if self.manager_date else None,
            'ep_review_user_id': self.ep_review_user_id.name if self.ep_review_user_id else None,
            'ep_review_time': self.ep_review_time if self.ep_review_time else None,
            'preliminary_clearance_user_id': self.preliminary_clearance_user_id.name if self.preliminary_clearance_user_id else None,
            'preliminary_clearance_time': self.preliminary_clearance_time if self.preliminary_clearance_time else None,
            'draft_dele_user_id': self.draft_dele_user_id.name if self.draft_dele_user_id else None,
            'draft_dele_time': self.draft_dele_time if self.draft_dele_time else None,
            'final_clearance_user_id': self.final_clearance_user_id.name if self.final_clearance_user_id else None,
            'final_clearance_time': self.final_clearance_time if self.final_clearance_time else None,
            'ep_sign_off_user_id': self.ep_sign_off_user_id.name if self.ep_sign_off_user_id else None,
            'ep_sign_off_time': self.ep_sign_off_time if self.ep_sign_off_time else None,
            'final_delivered_user_id': self.final_delivered_user_id.name if self.final_delivered_user_id else None,
            'final_delivered_time': self.final_delivered_time if self.final_delivered_time else None,
            'complete_user_id': self.complete_user_id.name if self.complete_user_id else None,
            'complete_time': self.complete_time if self.complete_time else None
        }
        return self.env.ref(
            'crowe_erp.action_report_control_sheet').report_action(self,
                                                                   data=data)

    def action_final_report(self):
        self.write({
            'final_delivered_user_id': self.env.user.id,
            'final_delivered_time': fields.Datetime.now(),
            'state': 'deliver_final_report'
        })

    def action_start_field_work(self):
        self.write({
            'field_work_started_user_id': self.env.user.id,
            'field_work_started_time': fields.Datetime.now(),
            'state': 'field_work_started'
        })

    def action_complete_field_work(self):
        if len(self.timesheet_ids) != 0:
            if self.sale_line_id.product_id.categ_id.id == self.env.ref(
                    'crowe_erp.product_category_task_type_medium').id:
                self.write({
                    'field_work_complete_user_id': self.env.user.id,
                    'fo_completed_time': fields.Datetime.now(),
                    'state': 'reviewer_sign_off'
                })
            else:
                self.write({
                    'field_work_complete_user_id': self.env.user.id,
                    'fo_completed_time': fields.Datetime.now(),
                    'state': 'field_work_completed'
                })
        else:
            raise ValidationError(
                "You can't complete field work without timesheet")

    def action_start_supervisor_check(self):
        self.write({
            'supervisor_user_id': self.env.user.id,
            'supervisor_time': fields.Datetime.now(),
            'state': 'supervisor_sign_off',
            'user_ids': [(4, self.supervisor_id.id)]
        })

    def action_start_reviewer_check(self):
        self.write({
            'manager_review_user_id': self.env.user.id,
            'manager_date': fields.Datetime.now(),
            'state': 'reviewer_sign_off',
            'user_ids': [(4, self.reviewed_id.id), (4, self.comment_id.id)]
        })

    def action_engagement_partner(self):
        self.write({
            'ep_review_user_id': self.env.user.id,
            'ep_review_time': fields.Datetime.now(),
            'state': 'engagement_partner',
            'user_ids': [(4, self.engagement_partner_id.id),
                         (4, self.engagement_comments_id.id),
                         (4, self.quality_reviewer_id.id)] if self.has_need_quality_check else [
                (4, self.engagement_partner_id.id),
                (4, self.engagement_comments_id.id)]
        })

    def action_draft_issue(self):
        if not self.full_invoice_check:
            if self.project_id.invoice_type == 'combine':
                line_ids = []
                for rec in self.env['work.order'].search(
                        [('project_id', '=', self.project_id.id)]):
                    line_ids.append((0, 0, {
                        'product_id': rec.task_id.sale_line_id.product_id.id,
                        'name': 'Remaining payment',
                        'company_id': self.env.company.id,
                        'price_unit': int(
                            rec.task_id.sale_line_id.price_subtotal) - int(
                            rec.task_id.invoice_amount),
                        'task_id': rec.task_id.id
                    }))
                    rec.task_id.write({
                        'full_invoice_check': True
                    })
                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'project_id':self.project_id.id,
                    'partner_id': self.sale_order_id.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'crowe_invoice_type': 'remaining',
                    'invoice_line_ids': line_ids
                })
                invoice_line_ids = []
                for rec in invoice.invoice_line_ids:
                    invoice_line_ids.append((4, rec.id))
                if self.sale_line_id.product_id.categ_id.id == self.env.ref(
                        'crowe_erp.product_category_task_type_short').id:
                    self.write({
                        'preliminary_clearance_user_id': self.env.user.id,
                        'preliminary_clearance_time': fields.Datetime.now(),
                        'state': 'deliver_final_report'
                    })
                elif self.sale_line_id.product_id.categ_id.id == self.env.ref(
                        'crowe_erp.product_category_task_type_medium').id:
                    self.write({
                        'preliminary_clearance_user_id': self.env.user.id,
                        'preliminary_clearance_time': fields.Datetime.now(),
                        'state': 'preliminary_clearance'
                    })
                else:
                    self.write({
                        'preliminary_clearance_user_id': self.env.user.id,
                        'preliminary_clearance_time': fields.Datetime.now(),
                        'state': 'preliminary_clearance',
                        'user_ids': [(4, self.draft_check_user_id.id),
                                     (4, self.draft_compared_user_id.id),
                                     (4, self.draft_checked_user_id.id)]
                    })
                self.sale_line_id.write({
                    'invoice_lines': invoice_line_ids
                })
            elif self.project_id.invoice_type == 'individual':
                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': self.project_id.sale_order_id.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'project_id':self.project_id.id,
                    'task_id': self.id,
                    'crowe_invoice_type': 'remaining',
                    'invoice_line_ids': [(0, 0, {
                        'product_id': self.sale_line_id.product_id.id,
                        'name': 'Remaining payment',
                        'company_id': self.env.company.id,
                        'price_unit': int(
                            self.sale_line_id.price_subtotal) - int(
                            self.invoice_amount)
                    })]
                })
                self.write({
                    'full_invoice_check': True
                })
                self.sale_line_id.write({
                    'invoice_lines': [(4, invoice.invoice_line_ids.id)]
                })
        if self.sale_line_id.product_id.categ_id.id == self.env.ref(
                'crowe_erp.product_category_task_type_short').id:
            self.write({
                'preliminary_clearance_user_id': self.env.user.id,
                'preliminary_clearance_time': fields.Datetime.now(),
                'state': 'deliver_final_report'
            })
        elif self.sale_line_id.product_id.categ_id.id == self.env.ref(
                'crowe_erp.product_category_task_type_medium').id:
            self.write({
                'preliminary_clearance_user_id': self.env.user.id,
                'preliminary_clearance_time': fields.Datetime.now(),
                'state': 'preliminary_clearance'
            })
        else:
            self.write({
                'preliminary_clearance_user_id': self.env.user.id,
                'preliminary_clearance_time': fields.Datetime.now(),
                'state': 'preliminary_clearance',
                'user_ids': [(4, self.draft_check_user_id.id),
                             (4, self.draft_compared_user_id.id),
                             (4, self.draft_checked_user_id.id)]
            })

    def action_deliver_report(self):
        if self.task_flow_type == 'medium':
            self.write({
                'draft_dele_user_id': self.env.user.id,
                'draft_dele_time': fields.Datetime.now(),
                'state': 'final_clearance'
            })
        else:
            self.write({
                'draft_dele_user_id': self.env.user.id,
                'draft_dele_time': fields.Datetime.now(),
                'state': 'draft_report_delivered'
            })

    def action_final_clearance(self):
        if self.task_flow_type == 'medium':
            self.write({
                'final_clearance_user_id': self.env.user.id,
                'final_clearance_time': fields.Datetime.now(),
                'state': 'final_clearance'
            })
        elif not self.letter_of_rep_check_head or not self.draft_duly_check or not self.final_tbalance_check or not self.pending_check or not self.compared_agreed_check:
            raise ValidationError("Please check the mandatory details")
        else:
            self.write({
                'final_clearance_user_id': self.env.user.id,
                'final_clearance_time': fields.Datetime.now(),
                'state': 'final_clearance'
            })

    def action_engagement_partner_signed_off(self):
        self.write({
            'ep_sign_off_user_id': self.env.user.id,
            'ep_sign_off_time': fields.Datetime.now(),
            'state': 'audit_partner_sign_off',
            'user_ids': [(4, self.final_clearance_aud_partner_id.id)]})

    def action_complete_task(self):
        self.write({
            'complete_user_id': self.env.user.id,
            'complete_time': fields.Datetime.now(),
            'state': 'complete'
        })

    def action_view_wo(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "work.order",
            "name": _("Work Order"),
            "views": [[False, "tree"], [False, "form"]],
            "context": {'default_task_id': self.id},
            "domain": [["task_id", "=", self.id]],
        }

    def action_set_to_complete(self):
        self.write({
            'state': 'complete'
        })
