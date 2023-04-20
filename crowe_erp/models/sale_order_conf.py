from odoo import models, fields, api
from odoo.addons.sale.models.sale_order import READONLY_FIELD_STATES
from odoo.exceptions import ValidationError
import base64
from num2words import num2words


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    loe_count = fields.Integer(default=-1)
    loe_received = fields.Boolean(
        string='Engagement Letter Signed')
    state = fields.Selection(
        selection=[
            ('draft', "Proposal"),
            ('approve', "Proposal Approved"),
            ('sent', "Proposal Sent"),
            ('loe', "LOE Send"),
            ('sale', "Sales Order"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template',
        string="Proposal Template",
        compute='_compute_sale_order_template_id',
        store=True, readonly=False, check_company=True, precompute=True,
        states=READONLY_FIELD_STATES,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet',
                                    ondelete='cascade', copy=False)
    validity_date = fields.Date(
        string="Year Ending",
        compute='_compute_validity_date',
        store=True, readonly=False, copy=False, precompute=True,
        states=READONLY_FIELD_STATES)

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        compute='_compute_payment_term_id',
        default=lambda self: self.env.ref(
            'account.account_payment_term_immediate').id,
        store=True, readonly=False, precompute=True, check_company=True,
        # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    def action_confirm(self):
        if self.loe_received:
            self.cost_sheet_id.write({
                'used_check': True
            })
            return super().action_confirm()
        else:
            raise ValidationError("Confirm LOE received or not")

    def action_approve_proposal(self):
        self.write({
            'state': 'approve'
        })

    def send_LOE(self):
        self.ensure_one()
        self.write({
            'loe_count': self.loe_count + 1
        })
        context = {
            'default_sale_order_id': self.id
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'send.loe.wizard',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': context,
        }


    # onchange methods
    @api.onchange('cost_sheet_id')
    def _onchange_cost_sheet_id(self):
        cost_sheet_template = self.cost_sheet_id
        order_lines_data = [fields.Command.clear()]
        order_lines_data += [
            fields.Command.create(line._prepare_order_line_values())
            for line in cost_sheet_template.service_product_ids
        ]
        self.order_line = order_lines_data
        self.validity_date = self.cost_sheet_id.year_ending_date


class InheritQuotationTemplate(models.Model):
    _inherit = 'sale.order.template'

    name = fields.Char(string="Proposal Template", required=True)


class InheritSaleSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_sale_order_template = fields.Boolean(
        "Proposal Templates",
        implied_group='sale_management.group_sale_order_template')
    use_quotation_validity_days = fields.Boolean(
        "Default Proposal Validity",
        config_parameter='sale.use_quotation_validity_days')
    module_sale_quotation_builder = fields.Boolean(string="Proposal Builder")


class WizardLOESend(models.TransientModel):
    _name = 'send.loe.wizard'
    _description = 'Wizard for configuring the mail cont' \
                   'end before sending loe'
    # _log_access = True

    partner_ids = fields.Many2many('res.partner',
                                   domain=[('type', '!=', 'private')])
    subject = fields.Char('Subject', related='template_id.subject',
                          readonly=False)
    body = fields.Html('Contents',
                       render_engine='qweb')
    attachment_ids = fields.Many2many('ir.attachment')
    sale_order_id = fields.Many2one('sale.order', string='sale order')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    template_id = fields.Many2one('mail.template',
                                  default=lambda self: self.env.ref(
                                      'crowe_erp.loe_email_template'))

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        count = self.env['ir.sequence'].search([('code', '=', 'sale.order')]).padding - len(
            str(self.env['ir.sequence'].search([('code', '=', 'sale.order')]).number_next_actual))
        seq = count * "0" + str(self.env['ir.sequence'].search([('code', '=', 'sale.order')]).number_next_actual - 1)
        data = {
            'sale_order': self.sale_order_id,
            'ref': "LOE/" + seq + "/CMG/" + str(
                fields.Date.today().year) + "/" + self.sale_order_id.loe_count * 'R' if self.sale_order_id.loe_count > 0 else "LOE/" + seq + "/CMG/" + str(
                fields.Date.today().year),
            'sale_order_total': num2words(
                round(self.sale_order_id.amount_total), to='ordinal')
        }
        report = self.env.ref('crowe_erp.action_letter_of_engagement')
        report_template_id = self.env.ref(
            'crowe_erp.action_letter_of_engagement')._render_qweb_pdf(report,
                                                                      data=data)
        b64_pdf = base64.b64encode(report_template_id[0]).decode()
        ir_values = {
            'name': 'LOE',
            'type': 'binary',
            'datas': b64_pdf,
            'store_fname': 'b64_pdf',
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        }
        attachment1 = self.env['ir.attachment'].create(ir_values)
        self.write({
            'attachment_ids': attachment1,
            'partner_ids': self.sale_order_id.partner_id
        })

    def action_send_mail(self):
        email_values = {'email_to': self.partner_ids.email,
                        'email_from': self.company_id.email,
                        'subject': self.subject,
                        "attachment_ids": [rec.id for rec in self.attachment_ids]}
        self.env.ref('crowe_erp.loe_email_template').send_mail(
            self.id, email_values=email_values, force_send=True)
        if self.sale_order_id.state == 'approve':
            self.sale_order_id.write({
                'state': 'loe'
            })
        return True
