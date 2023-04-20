from odoo import fields, models, api
import requests
import json
from odoo.exceptions import ValidationError
import re
import string


class InheritSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char(string='API Key',
                          config_parameter='mailercloud_connector.api_key')
    api_check_mailer_cloud = fields.Boolean(string='Check',
                                            config_parameter='mailercloud_connector.api_check_mailer_cloud',
                                            default=False)

    @api.onchange('api_key')
    def _onchange_api_key(self):
        self.env['ir.config_parameter'].set_param(
            'mailercloud_connector.api_check_mailer_cloud', False)

    def action_check_api(self):
        print("called")
        self.env.cr.execute("""truncate contact_list""")
        self.env.cr.execute("""truncate audience_list cascade""")
        self.env.cr.execute("""truncate mailer_cloud_campaign cascade""")
        self.get_list_details()  # method for fetching all campaign details from mailer cloud
        self.get_campaign_details()

    def get_list_count(self):

        # method for fetching list count from mailer cloud
        url = "https://cloudapi.mailercloud.com/v1/lists/search"

        payload = json.dumps({
            "limit": 100,
            "list_type": 1,
            "page": 1,
            "search_name": "",
            "sort_field": "name",
            "sort_order": "asc"
        })
        headers = {
            'Authorization': self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_key'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            self.env['ir.config_parameter'].sudo().set_param(
                'mailercloud_connector.api_check_mailer_cloud', True)
            # print(response.text)
            page_count = 0
            if response.json()['list_count'] % 100 != 0:
                page_count += response.json()['list_count'] // 100
                page_count += 1
            else:
                page_count += response.json()['list_count'] // 100
            return page_count
        else:
            print(response.json())
            try:
                raise ValidationError(response.json()['errors'][0]['message'])
            except:
                # raise ValidationError("Server error")
                pass

    def get_list_details(self):
        count = self.get_list_count()
        # method for getting all details of list from mailer cloud
        for i in range(1, int(count) + 1):
            print(i)
            url = "https://cloudapi.mailercloud.com/v1/lists/search"

            payload = json.dumps({
                "limit": 100,
                "list_type": 1,
                "page": i,
                "search_name": "",
                "sort_field": "name",
                "sort_order": "asc"
            })
            headers = {
                'Authorization': self.env['ir.config_parameter'].get_param(
                    'mailercloud_connector.api_key'),
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers,
                                        data=payload)
            # if response.status_code == 4
            if response.status_code == 200:
                for rec in [rec for rec in response.json()['data'] if
                            int(rec['contact_count']) > 0]:
                    print("list function_called", rec['id'])
                    self.env.cr.execute("""INSERT INTO audience_list(audience_list_id,name,open_rate,last_updated)
                                                VALUES('%s','%s',%s,'%s')""" % (
                        rec['id'], rec['name'], rec['open_percentage'],
                        fields.Date.today()))
                    self.env.cr.execute(
                        """SELECT id,audience_list_id FROM audience_list ORDER BY ID DESC LIMIT 1""")
                    record_id = self.env.cr.dictfetchall()
                    self.get_contact_details(record_id[0]['id'],
                                             record_id[0][
                                                 'audience_list_id'])
            else:
                print(response.json())
                try:
                    raise ValidationError(
                        response.json()['errors'][0]['message'])
                except:
                    # raise ValidationError("Server error")
                    pass

    def get_contact_details(self, id, mailer_cloud_id):
        # method for fetching all contact details of particular list
        url = "https://cloudapi.mailercloud.com/v1/contact/search/" + \
              mailer_cloud_id

        payload = json.dumps({
            "limit": 100,
            "page": 1,
            "search": ""
        })
        headers = {
            'Authorization': self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_key'),
            'Content-Type': 'application/json'
        }

        response1 = requests.request("POST", url, headers=headers,
                                     data=payload)
        if response1.status_code == 200:
            self.env.cr.execute(
                """UPDATE audience_list SET contact_count = %s WHERE audience_list_id = '%s'""" % (
                    response1.json()['contact_count'], mailer_cloud_id))
            print('contact function called..........')
            for record in response1.json()['data']:
                self.env.cr.execute("""INSERT INTO contact_list(contact_id,name,middle_name,last_name,email,phone,country,city,zip,state,audience_list_id,contact_type)
                                                    VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
                    record['id'], record['name'], record['middle_name'],
                    record['last_name'], record['email'],
                    record['phone'], record['country'], record['city'],
                    record['zip'], record['state'],
                    id, 'active'))
        else:
            print(response1.json())
            try:
                raise ValidationError(response1.json()['errors'][0]['message'])
            except:
                # raise ValidationError("Server error")
                pass

    def get_campaign_details(self):
        # method for fetching all campaign details from mailer cloud
        url = "https://cloudapi.mailercloud.com/v1/campaign/list"

        payload = json.dumps({
            "date_to": str(fields.Date.today()),
            "limit": 100,
            "page": 1
        })
        headers = {
            'Authorization': self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_key'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        if response.status_code == 200:
            try:
                for record in response.json()['data']:
                    print('campaign function called.......')
                    state = ''
                    if record['status'] == 'Processing':
                        state = 'processing'
                    elif record['status'] == 'Paused':
                        state = 'paused'
                    elif record['status'] == 'Scheduled':
                        state = 'schedule'
                    elif record['status'] == 'Draft':
                        state = 'draft'
                    elif record['status'] == 'Finished':
                        state = 'finished'
                    elif record['status'] == 'Aborted':
                        state = 'aborted'
                    body_arch = record['html']
                    mail_body = body_arch.replace("\'", "\"")
                    self.env.cr.execute("""INSERT INTO mailer_cloud_campaign(campaign_id,name,subject,sender_email,sender_name,send,sent_percentage,delivered,delivered_percentage,opens,open_percentage,clicks,clicks_percentage,state,create_date,write_date,body_arch,mailing_model_id)
                                                                                   VALUES('%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s','%s','%s',%s)""" % (
                        record['id'], record['name'], record['subject'],
                        record['sender']['sender_email'],
                        record['sender']['sender_name'],
                        record['report_summary']['sent'],
                        int(float(
                            record['report_summary']['sent_percentage'])),
                        record['report_summary']['delivered'],
                        int(float(
                            record['report_summary']['delivered_percentage'])),
                        record['report_summary']['opens'],
                        int(float(
                            record['report_summary']['open_percentage'])),
                        record['report_summary']['clicks'],
                        int(float(
                            record['report_summary']['clicks_percentage'])),
                        state, record['created_date'], record['modified_date'],
                        mail_body, self.env.ref(
                            'mailercloud_connector.model_audience_list').id))
                    if record['recepiant']['lists'].split(","):
                        for rec in record['recepiant']['lists'].split(","):
                            if self.env['audience.list'].search(
                                    [('name', '=', rec)]):
                                self.env.cr.execute(
                                    """SELECT id FROM mailer_cloud_campaign ORDER BY ID DESC LIMIT 1""")
                                record_id = self.env.cr.dictfetchall()
                                self.env.cr.execute("""INSERT INTO audience_list_mailer_cloud_campaign_rel(mailer_cloud_campaign_id,audience_list_id)
                                                                                VALUES(%s,%s)""" % (
                                    record_id[0]['id'],
                                    self.env['audience.list'].search(
                                        [('name', '=', rec)]).id))
            except Exception as e:
                print(e)
                pass
        else:
            print(response.json())
            try:
                raise ValidationError(response.json()['errors'][0]['message'])
            except:
                print("llllllllll")
                # raise ValidationError("Server error")
                pass
