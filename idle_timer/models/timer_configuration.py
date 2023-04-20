from odoo import models, fields


class IdleTimer(models.Model):
    _inherit = 'survey.survey'

    is_question_time_limit = fields.Boolean()
    question_time_limit = fields.Float(string="Question Time Limit", default=1)
    idle_timer = fields.Float(string="Idle Timer")
