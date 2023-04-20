from odoo import fields, models


class AudienceSegment(models.Model):
    _name = 'audience.segment'

    segment = fields.Char()
