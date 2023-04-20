from odoo import fields, models
import xmlrpc.client


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    instance_url = fields.Char(string='Odoo Instance Url', config_parameter='cloud_cluster_import.instance_url')
    database_name = fields.Char(string='Database Name', config_parameter='cloud_cluster_import.database_name')
    api_key = fields.Char(string='Api Key', config_parameter='cloud_cluster_import.api_key')
    user_name = fields.Char(string='User Name', config_parameter='cloud_cluster_import.user_name')

    def import_record_cloud(self):
        data_url = self.env['ir.config_parameter'].sudo().get_param(
            'cloud_cluster_import.instance_url')  # odoo instance url
        database = self.env['ir.config_parameter'].sudo().get_param(
            'cloud_cluster_import.database_name')  # database name
        user = self.env['ir.config_parameter'].sudo().get_param('cloud_cluster_import.user_name')  # username
        password = self.env['ir.config_parameter'].sudo().get_param('cloud_cluster_import.api_key')  # api key
        common_auth = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(data_url))
        print(database, "ddddddd", user, "ddd", password)
        uid = common_auth.authenticate(database, user, password, {})
        data_model = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(data_url))
        print('sssssssssssssssss', data_model)
        print(";;;;;;;;;;;;;;;;",
              data_model.execute_kw(database, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]]))
        print("kkkkkkkk")
