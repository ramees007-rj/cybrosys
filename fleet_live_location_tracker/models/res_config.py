from odoo import models, fields


class ResConfigSettingsInherit(models.TransientModel):
    """Inherit res.config.settings to set google map api"""
    _inherit = 'res.config.settings'

    google_map_api = fields.Char(string='Google Map API',
                                 config_parameter='fleet.google_map_api')
    traccar_server_url = fields.Char(string='Traccar Server URL',
                             config_parameter='fleet.server_url')
    traccar_email = fields.Char(string='Traccar Email',
                        config_parameter='fleet.traccar_email')
    traccar_password = fields.Char(string="Traccar Password",
                           config_parameter='fleet.traccar_password')
