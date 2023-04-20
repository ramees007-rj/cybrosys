from odoo import fields, models, api


class Questionnaire(models.Model):
    _name = 'questionnaire'
    _description = 'Collecting data through survey and store here'

    @api.depends('partner_id')
    def _compute_name(self):
        for rec in self:
            rec.name = 'Questionnaire/' + rec.partner_id.name

    name = fields.Char(compute='_compute_name', precompute=True,store=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    constitution = fields.Char(string='Constitution')
    comm_reg_no = fields.Char(string="Commercial Registration Number")
    members = fields.Text(string='Members')
    accounting_period = fields.Char(string='Accounting Period')
    reg_capital = fields.Char(string="Registered capital (RO)")
    main_activities = fields.Text(string="Main Activities")
