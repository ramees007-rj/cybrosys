from odoo import fields, models, api, _


class ProjectInherit(models.Model):
    _inherit = 'project.project'

    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet',
                                    related='sale_order_id.cost_sheet_id')
    estimated_hours = fields.Float(related='cost_sheet_id.total_hours',
                                   string='Budgeted Hours', store=True)
    amount_untaxed = fields.Monetary(related='sale_order_id.amount_untaxed',
                                     string='Amount', store=True)
    amount_tax = fields.Monetary(related='sale_order_id.amount_tax',
                                 string='Vat Amount', store=True)
    amount_total = fields.Monetary(related='sale_order_id.amount_total',
                                   string='Total Amount', store=True)
    invoice_type = fields.Selection(
        selection=[('combine', 'Combined'), ('individual', 'Separate')],
        string='Invoice Type', default='combine')
    sequence = fields.Char(string="Project Number", readonly=True,
                           required=True,
                           copy=False, default='New')
    name = fields.Char("Name", index='trigram', required=True, tracking=True,
                       translate=True, default_export_compatible=True,
                       help="Name of your project. It can be anything you want e.g. the name of a customer or a service.")
    task_assignees_ids = fields.Many2many('res.users', 'task_assignees_rel', string="Task Assignees",
                                          compute='_compute_task_assignees_ids')

    def action_view_tasks_main(self):
        action = self.env['ir.actions.act_window'].with_context(
            {'active_id': self.id})._for_xml_id(
            'project.act_project_project_2_project_task_all')
        return action

    @api.model
    def create(self, vals_list):
        vals_list['sequence'] = self.env['ir.sequence'].next_by_code(
            'project.crowe.sequence') or _('New')
        customer_name = self.env['res.partner'].browse(
            vals_list['partner_id']).name
        vals_list['name'] = vals_list['sequence'] + customer_name
        return super(ProjectInherit, self).create(vals_list)

    @api.depends('task_ids')
    def _compute_task_assignees_ids(self):
        for rec in self:
            for id in rec._origin.task_ids.mapped('user_ids.id'):
                rec.write({
                    'task_assignees_ids': [(4, id)]
                })
