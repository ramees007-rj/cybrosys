from odoo import models, fields, api
from odoo.exceptions import UserError


class EmployeeTransfer(models.Model):
    _inherit = 'hr.employee'

    transfer_id = fields.Integer()

    def request(self):
        context = {'default_employee_id': self.id}
        return {
            'name': 'Transfer',
            'res_model': 'transfer',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': context,
            'target': 'current'
        }


class EmployeeTransferPortal(models.Model):
    _name = 'transfer'
    _description = 'Employee Transfer Portal'

    name = fields.Char(compute='_compute_name')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    company_id = fields.Many2one(string='Company    ',
                                 related='employee_id.company_id')
    transfer_to_id = fields.Many2one('res.company', string='Transfer TO')
    note = fields.Text(string='Note')
    state = fields.Selection([('transfer', 'Transfer'),
                              ('done', 'Done'),
                              ('reject', 'Rejected')], string='Status',
                             required=True, readonly=True, copy=False,
                             default='transfer')
    check = fields.Boolean(default=False)

    def action_approve(self):
        self.employee_id.active = False
        self.env['hr.employee'].create({
            'name': self.employee_id.name,
            'company_id': self.transfer_to_id.id
        })
        self.check = True
        self.state = 'done'

    def action_reject(self):
        self.check = True
        self.state = 'reject'

    def _compute_name(self):
        self.name = self.employee_id.name + " " + "Transfer"
