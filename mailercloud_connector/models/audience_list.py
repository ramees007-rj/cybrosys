from odoo import fields, models, api
from odoo.exceptions import ValidationError
import requests
import json
import datetime


class AudienceList(models.Model):
    _name = 'audience.list'
    _description = 'Audience list details'

    audience_list_id = fields.Char()
    name = fields.Char(string="Name", required=True)
    last_updated = fields.Date(string='Last Updated',
                               compute='_compute_last_updated', store=True)
    contact_count = fields.Integer(string='contact',
                                   compute='_compute_contact_count',
                                   store=True)
    open_rate = fields.Float(string='Open Rate', readonly=True)
    contact_ids = fields.One2many('contact.list', 'audience_list_id',
                                  string='Contacts')

    # name validation
    @api.onchange('name')
    def che(self):
        if self.name in self.search([]).mapped('name'):
            raise ValidationError("Contact list name is already exists")

    @api.depends('write_date')
    def _compute_last_updated(self):
        for rec in self:
            rec.last_updated = rec.write_date

    # calculating count of contact_ids
    @api.depends('contact_ids')
    def _compute_contact_count(self):
        for rec in self:
            rec.contact_count = len(rec.contact_ids)

    @api.model
    def create(self, vals_list):
        # api call for  creating list in mailer cloud app
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            if len(vals_list['contact_ids']) == 0:
                raise ValidationError("You have to add at least one contact")
            print(vals_list)
            url = "https://cloudapi.mailercloud.com/v1/list"
            payload = json.dumps({
                "list_type": 1,
                "name": vals_list['name']
            })
            headers = {
                'Authorization': self.env['ir.config_parameter'].get_param(
                    'mailercloud_connector.api_key'),
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers,
                                        data=payload)
            print("hhhhhhhhhh", response.text)
            try:
                vals_list['audience_list_id'] = response.json()['id']
            except:
                pass
            return super(AudienceList, self).create(vals_list)
        else:
            raise ValidationError("Please check your Api key")

    def write(self, vals):
        # api call for updating values in particular list
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            print(vals)
            data = {'name': self.name}
            for key, value in vals.items():
                if key in ('contact_ids', 'audience_list_id'):
                    continue
                else:
                    data[key] = value
            try:
                url = "https://cloudapi.mailercloud.com/v1/list/" + self.audience_list_id

                payload = json.dumps(data)
                headers = {
                    'Authorization': self.env['ir.config_parameter'].get_param(
                        'mailercloud_connector.api_key'),
                    'Content-Type': 'application/json'
                }

                response = requests.request("PATCH", url, headers=headers,
                                            data=payload)

                print("aaaaaaaaa", response.text)
            except:
                pass
            return super(AudienceList, self).write(vals)
        else:
            raise ValidationError("Please check your Api key")

    def unlink(self):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            # api call for deleting list in mailer cloud
            if self.create_date:
                # checking deletion date is greater than create date
                if self.create_date + datetime.timedelta(
                        days=14) < fields.Datetime.today():
                    try:
                        url = "https://cloudapi.mailercloud.com/v1/list/" + self.audience_list_id

                        payload = ""
                        headers = {
                            'Authorization': self.env[
                                'ir.config_parameter'].get_param(
                                'mailercloud_connector.api_key'),
                            'Content-Type': 'application/json'
                        }

                        response = requests.request("DELETE", url,
                                                    headers=headers,
                                                    data=payload)

                        print(response.text)
                    except:
                        pass
                    return super(AudienceList, self).unlink()
                else:
                    raise ValidationError(
                        "You are possible to delete the list only after 14 days")
            else:
                return super(AudienceList, self).unlink()
        else:
            raise ValidationError("Please Check your Api key")
