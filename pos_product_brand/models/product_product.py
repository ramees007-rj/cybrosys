# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    refund_employee_ids = fields.Many2many('hr.employee',config_parameter='pos_product_brand.refund_employee_ids')

class PosConfigSettings(models.Model):
    _inherit = "pos.config"