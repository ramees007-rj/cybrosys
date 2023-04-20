from odoo import fields, models
from odoo.exceptions import ValidationError


class InheritPayrollRule(models.Model):
    _inherit = 'hr.salary.rule'

    debit_account_id = fields.Many2one('account.account', string="Debit Account")
    credit_account_id = fields.Many2one('account.account', string="Credit Account")


class InheritPayroll(models.Model):
    _inherit = 'hr.payslip'


    def action_payslip_done(self):
        res = super().action_payslip_done()
        line_ids = []
        for rec in self.line_ids:
            if rec.salary_rule_id.debit_account_id and rec.salary_rule_id.credit_account_id:
                line_ids.append((0, 0, {
                    'account_id': rec.salary_rule_id.debit_account_id.id,
                    'currency_id': self.env.company.currency_id.id,
                    'debit': rec.amount,
                    'credit': 0.0,
                }))
                line_ids.append((0, 0, {'account_id': rec.salary_rule_id.credit_account_id.id,
                                        'currency_id': self.env.company.currency_id.id, 'debit': 0.0,
                                        'credit': rec.amount}))
            elif rec.salary_rule_id.debit_account_id and not rec.salary_rule_id.credit_account_id or not rec.salary_rule_id.debit_account_id and rec.salary_rule_id.credit_account_id:
                raise ValidationError("Please configure accounts in the salary rule properly")
            else:
                continue
        self.env['account.move'].create({
            'move_type': 'entry',
            'ref': self.number,
            'date': fields.Date.today(),
            'line_ids': line_ids
        })
        return res
