from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

LOCKED_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'approve'}
}


class CostSheet(models.Model):
    _name = 'cost.sheet'
    _rec_name = 'reference_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    reference_no = fields.Char(string='Reference', copy=False, required=True,
                               readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', states=LOCKED_FIELD_STATES)
    year_ending_date = fields.Date("Year Ending", default=fields.Date.today(), states=LOCKED_FIELD_STATES)
    prepared_date = fields.Date(string='Prepared On',
                                default=fields.Date.today(), states=LOCKED_FIELD_STATES)
    prepared_user_id = fields.Many2one('res.users', string='Prepared By',
                                       default=lambda self: self.env.user, states=LOCKED_FIELD_STATES)
    cost_sheet_line_ids = fields.One2many('cost.sheet.line', 'cost_sheet_id',
                                          copy=True, states=LOCKED_FIELD_STATES)
    admin_expenses = fields.Float(string='Admin Expenses', states=LOCKED_FIELD_STATES)
    other_expenses = fields.Float(string='Other Expenses', states=LOCKED_FIELD_STATES)
    grand_total = fields.Float(string='Total', compute='_compute_grand_total')
    total_hours = fields.Float(string='Total Hours')
    service_product_ids = fields.One2many('cost.sheet.service.line', 'cost_id',
                                          string='Service',
                                          states=LOCKED_FIELD_STATES,
                                          ondelete='cascade', copy=True)
    service_ids = fields.Many2many('product.product',
                                   compute='_compute_service_ids')
    state = fields.Selection(
        [('draft', 'Draft'), ('approve', 'Approved')], string='State',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        default='draft')

    used_check = fields.Boolean(copy=False)

    def action_approve(self):
        self.write({
            'state': 'approve',
            'reference_no': self.env['ir.sequence'].next_by_code(
                'cost.sheet') or _('New')
        })

    def unlink(self):
        for rec in self:
            if rec.state == 'approve':
                raise ValidationError("Approved cost sheet cannot be deleted")
            else:
                return super().unlink()

    @api.depends('service_product_ids')
    def _compute_service_ids(self):
        for rec in self:
            rec.write({
                'service_ids': rec.service_product_ids.mapped('product_id.id')
            })

    @api.depends('cost_sheet_line_ids', 'admin_expenses', 'other_expenses')
    def _compute_grand_total(self):
        for cost_sheet in self:
            cost_sheet.write({
                'grand_total': sum(
                    cost_sheet.cost_sheet_line_ids.mapped(
                        'total')) + cost_sheet.admin_expenses + cost_sheet.other_expenses,
                'total_hours': sum(
                    cost_sheet.cost_sheet_line_ids.mapped(
                        'man_hours'))
            })

    # @api.model
    # def create(self, vals):
    #     if vals.get('reference_no', _('New')) == _('New'):
    #         vals['reference_no'] =
    #     res = super(CostSheet, self).create(vals)
    #     return res


class CostSheetLines(models.Model):
    _name = 'cost.sheet.line'

    designation_id = fields.Many2one('hr.job', string='Designation')
    cost = fields.Monetary(related='designation_id.minimum_cost',
                           string='Cost', readonly=False)
    man_hours = fields.Float(string='Man Hours')
    total = fields.Float(string='Total', compute='_compute_total')
    product_id = fields.Many2one('product.product', string='Service')
    cost_sheet_id = fields.Many2one('cost.sheet')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Currency",
    )

    @api.depends('man_hours')
    def _compute_total(self):
        for rec in self:
            rec.write({
                'total': rec.cost * rec.man_hours
            })


class CostSheetServiceLine(models.Model):
    _name = 'cost.sheet.service.line'
    _description = 'Cost Sheet Service line'

    product_id = fields.Many2one('product.product')
    name = fields.Text(
        string="Description",
        compute='_compute_name',
        store=True, readonly=False, precompute=True,
        required=True,
        translate=True)
    cost_id = fields.Many2one('cost.sheet')

    # === COMPUTE METHODS ===#

    @api.depends('product_id')
    def _compute_name(self):
        for option in self:
            if not option.product_id:
                continue
            print(option.cost_id.year_ending_date)
            option.name = option.product_id.name + " for year ending " + str(
                option.cost_id.year_ending_date.strftime("%d-%m-%Y"))

    def _prepare_order_line_values(self):
        """ Give the values to create the corresponding order line.

        :return: `sale.order.line` create values
        :rtype: dict
        """
        self.ensure_one()
        return {
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_qty': 1,
        }
