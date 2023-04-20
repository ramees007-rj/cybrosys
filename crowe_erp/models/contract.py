from odoo import fields, models


class ContractInherit(models.Model):
    _inherit = 'hr.contract'

    mobile_allowance = fields.Monetary(string='Mobile Allowance', tracking=True, help="Mobile Allowance.")
    outstation_allowance = fields.Monetary(string='Outstation allowance', tracking=True, help="Outstation allowance.")
    incentives = fields.Monetary(string='Incentives', tracking=True, help="Incentives.")
    managerial_remuneration = fields.Monetary(string='Managerial remuneration', tracking=True,
                                              help="Managerial remuneration.")
    car_allowance = fields.Monetary(string='Car Allowance', tracking=True, help="Car Allowance.")
    conveyance_allowance = fields.Monetary(string='Conveyance Allowance', tracking=True, help="Conveyance Allowance.")
    salary_advance = fields.Monetary(string='Salary advance', tracking=True, help="Conveyance Allowance.")
    social_insurance = fields.Monetary(string='Social insurance', tracking=True,
                                       help="Social insurance - employee contribution.")
    fine = fields.Monetary(string='Fine', tracking=True, help="Fine.")

