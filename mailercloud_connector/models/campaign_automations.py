from odoo import fields, models, api


class CampaignAutomations(models.Model):
    _name = 'campaign.automation'

    test = fields.Char()
