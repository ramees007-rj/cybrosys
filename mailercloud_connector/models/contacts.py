from odoo import fields, models, api
from odoo.exceptions import ValidationError
import requests
import json
import datetime
import re


class ContactsList(models.Model):
    _name = 'contact.list'
    _sql_constraints = [
        ('name_email', 'unique (email)', 'Contact Email already exists!')
    ]
    contact_id = fields.Char()
    name = fields.Char(string='First Name')
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    country = fields.Char(string='Country')
    city = fields.Char(string='City')
    zip = fields.Char(string='Zip')
    state = fields.Char(string='State')
    audience_list_id = fields.Many2one('audience.list')
    contact_type = fields.Selection([
        ('active', 'active'),
        ('bounce', 'bounce'),
        ('abuse', 'abuse'),
        ('unsubscribe', 'unsubscribe'),
        ('suppressed', 'suppressed'),
    ], string='Contact Type', required=True, default='active')

    @api.onchange('email')
    def _onchange_email(self):
        if self.email:
            match = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')

    @api.model
    def create(self, vals_list):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            # api call for creating contact in mailer cloud
            print(vals_list)
            try:
                url = "https://cloudapi.mailercloud.com/v1/contacts"

                payload = json.dumps({
                    "list_id": self.env['audience.list'].browse(
                        vals_list['audience_list_id']).audience_list_id,
                    "email": vals_list['email'],
                    "contact_type": vals_list['contact_type'],
                    'middle_name': vals_list['middle_name'] if vals_list[
                        'middle_name'] else " ",
                    'last_name': vals_list['last_name'] if vals_list[
                        'last_name'] else " ",
                    'phone': vals_list['phone'] if vals_list['phone'] else " ",
                    'country': vals_list['country'] if vals_list[
                        'country'] else " ",
                    'city': vals_list['city'] if vals_list['city'] else " ",
                    'zip': vals_list['zip'] if vals_list['zip'] else " ",
                    'state': vals_list['state'] if vals_list['state'] else " ",
                    'name': vals_list['name'] if vals_list['name'] else " "

                })
                headers = {
                    'Authorization': self.env['ir.config_parameter'].get_param(
                        'mailercloud_connector.api_key'),
                    'Content-Type': 'application/json'
                }

                response1 = requests.request("POST", url, headers=headers,
                                             data=payload)
                print("ccccc", response1.text)
                vals_list['contact_id'] = response1.json()['id']
            except:
                pass
            return super(ContactsList, self).create(vals_list)
        else:
            raise ValidationError("Please check your Api key")

    def write(self, vals):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            # api call for updating contact in mailer cloud
            data = {}
            for key, value in vals.items():
                if key == ('contact_id', 'email'):
                    continue
                else:
                    data[key] = value
            try:
                url = "https://cloudapi.mailercloud.com/v1/contacts/" + self.contact_id

                payload = json.dumps(data)
                headers = {
                    'Authorization': self.env['ir.config_parameter'].get_param(
                        'mailercloud_connector.api_key'),
                    'Content-Type': 'application/json'
                }

                response = requests.request("PUT", url, headers=headers,
                                            data=payload)
                print(response.text)
            except:
                pass
            return super(ContactsList, self).write(vals)
        else:
            raise ValidationError("Please check your Api key")

    def unlink(self):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            print('function called')
            # api call for deleting contact in mailer cloud
            if self.create_date:
                # checking deletion date is greater than create date
                if self.create_date + datetime.timedelta(
                        days=14) < fields.Datetime.today():
                    try:
                        url = "https://cloudapi.mailercloud.com/v1/contacts/" + self.contact_id

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
                    return super(ContactsList, self).unlink()
                else:
                    raise ValidationError(
                        "You are possible to delete the contact only after 14 days")
            else:
                return super(ContactsList, self).unlink()
        else:
            raise ValidationError("Please check your Api key")
