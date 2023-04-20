from odoo import fields, models, api
from odoo.exceptions import ValidationError
import requests
import json
from datetime import datetime
import lxml
from pytz import timezone
import re

# Syntax of the data URL Scheme: https://tools.ietf.org/html/rfc2397#section-3
# Used to find inline images
image_re = re.compile(r"data:(image/[A-Za-z]+);base64,(.*)")


class Campaign(models.Model):
    _name = 'mailer.cloud.campaign'

    campaign_id = fields.Char()
    name = fields.Char(string='Campaign Name', required=True)
    subject = fields.Char(string='Subject Line', required=True)
    sender_email = fields.Char(string='From Id', required=True)
    sender_name = fields.Char(string='Sender Name', required=True)
    reply_email = fields.Char(string='Reply To', compute='_compute_reply_mail')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('schedule', 'Scheduled'),
        ('processing', 'Processing'),
        ('paused', 'Paused'),
        ('finished', 'Finished'),
        ('aborted', 'Aborted'),
        ('failed', 'Failed'),
    ], string='Status',
        default='draft', required=True,
        copy=False, tracking=True,
        group_expand='_group_expand_states')
    modified_date = fields.Datetime(string='Last Updated',
                                    compute='_compute_modified_date')
    body_arch = fields.Html(string='Body', translate=False, sanitize=False)
    body_html = fields.Html(string='Body converted to be sent by mail',
                            render_engine='qweb', sanitize=False)
    list_ids = fields.Many2many('audience.list', string='Lists', required=True)
    send = fields.Integer()
    sent_percentage = fields.Integer()
    delivered = fields.Integer()
    delivered_percentage = fields.Integer()
    opens = fields.Integer()
    open_percentage = fields.Integer()
    clicks = fields.Integer()
    clicks_percentage = fields.Integer()
    mailing_model_id = fields.Many2one(
        'ir.model', string='Recipients Model',
        ondelete='cascade', required=True,
        domain=[('is_mailing_enabled', '=', True)],
        default=lambda self: self.env.ref(
            'mailercloud_connector.model_audience_list').id)

    # @api.depends('mailing_model_id')
    # def _compute_mailing_model_real(self):
    #     for mailing in self:
    #         mailing.mailing_model_real = 'mailing.contact' if mailing.mailing_model_id.model == 'mailing.list' else mailing.mailing_model_id.model

    @api.depends('sender_email')
    def _compute_reply_mail(self):
        for rec in self:
            rec.reply_email = rec.sender_email

    @api.depends('write_date')
    def _compute_modified_date(self):
        for rec in self:
            rec.modified_date = rec.write_date

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    @api.model
    def create(self, vals_list):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            # api call for creating campaign in mailer cloud
            if vals_list['body_arch'] == False or len(
                    vals_list['list_ids'][0][2]) == 0:
                raise ValidationError("You are missing some mandatory fields")
            else:
                try:
                    url = "https://cloudapi.mailercloud.com/v1/campaign"
                    print(vals_list['body_arch'])
                    payload = json.dumps({
                        "html": self._convert_inline_images_to_urls(
                            vals_list['body_arch']),
                        "list_ids": self.env['audience.list'].browse(
                            vals_list['list_ids'][0][2]).mapped(
                            'audience_list_id'),
                        "name": vals_list['name'],
                        "sender": {
                            "sender_email": vals_list['sender_email'],
                            "sender_name": vals_list['sender_name']
                        },
                        "subject": vals_list['subject'],
                        "viewin_browser": True,
                    })
                    headers = {
                        'Authorization': self.env[
                            'ir.config_parameter'].get_param(
                            'mailercloud_connector.api_key'),
                        'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", url, headers=headers,
                                                data=payload)

                    print(response.text)
                    vals_list['campaign_id'] = response.json()['id']
                except:
                    pass
                return super(Campaign, self).create(vals_list)
        else:
            raise ValidationError("Please check your Api key")

    def write(self, vals):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            # api call for updating campaign in mailer cloud
            data = {}
            sender = {'sender_email': self.sender_email,
                      'sender_name': self.sender_name}
            for key, value in vals.items():
                print(key)
                if key in ('campaign_id', 'state','body_arch'):
                    continue
                elif key == 'body_html':
                    data['html'] = self._convert_inline_images_to_urls(value)
                elif key in ('sender_email', 'sender_name'):
                    sender[key] = value
                elif key == 'list_ids':
                    data[key] = self.env['audience.list'].browse(
                        vals['list_ids'][0][2]).mapped('audience_list_id')
                else:
                    data[key] = value
            if len(sender) > 0:
                data['sender'] = sender
            try:
                url = "https://cloudapi.mailercloud.com/v1/campaign/" + self.campaign_id

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
            return super(Campaign, self).write(vals)
        else:
            raise ValidationError("Please check your Api key")

    def action_schedule(self):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            self.ensure_one()
            action = self.env["ir.actions.actions"]._for_xml_id(
                "mailercloud_connector.campaign_schedule_date_action")
            action['context'] = dict(self.env.context,
                                     default_campaign_id=self.campaign_id,
                                     dialog_size='medium')
            return action
        else:
            raise ValidationError("Please check your Api key")

    def action_test_mail(self):
        if self.env['ir.config_parameter'].get_param(
                'mailercloud_connector.api_check_mailer_cloud'):
            self.ensure_one()
            action = self.env["ir.actions.actions"]._for_xml_id(
                "mailercloud_connector.campaign_test_mail_date_action")
            action['context'] = dict(self.env.context,
                                     default_campaign_id=self.campaign_id,
                                     dialog_size='medium')
            return action
        else:
            raise ValidationError("Please check your Api key")

    def _convert_inline_images_to_urls(self, body_html):
        """
        Find inline base64 encoded images, make an attachement out of
        them and replace the inline image with an url to the attachement.
        """

        def _image_to_url(b64image: bytes):
            print("function called")
            """Store an image in an attachement and returns an url"""
            attachment = self.env['ir.attachment'].create({
                'datas': b64image,
                'name': "cropped_image_mailing_{}".format(self.id),
                'type': 'binary', })

            attachment.generate_access_token()

            return '/web/image/%s?access_token=%s' % (
                attachment.id, attachment.access_token)

        modified = False
        root = lxml.html.fromstring(body_html)
        print("root",root)
        for node in root.iter('img'):
            match = image_re.match(node.attrib.get('src', ''))
            print('match',match)
            if match:
                mime = match.group(1)  # unsed
                image = match.group(2).encode()  # base64 image as bytes

                node.attrib['src'] = _image_to_url(image)
                modified = True

        if modified:
            return lxml.html.tostring(root, encoding='unicode')
        return body_html


class ScheduleCampaign(models.TransientModel):
    _name = 'mailer.cloud.schedule.campaign'
    _description = 'Schedule Campaign'

    schedule_date = fields.Datetime(string='Schedule for',
                                    default=fields.Datetime.now())
    campaign_id = fields.Char(required=True)

    def action_schedule_date(self):
        try:
            # api call for scheduling campaign in mailer cloud
            url = "https://cloudapi.mailercloud.com/v1/campaign/schedule/" + self.campaign_id
            payload = json.dumps({
                "scheduled_at": self.schedule_date.astimezone(
                    timezone(self.env.user.tz)).strftime(
                    '%Y-%m-%d %H:%M:%S')
            })
            headers = {
                'Authorization': self.env['ir.config_parameter'].get_param(
                    'mailercloud_connector.api_key'),
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers,
                                        data=payload)

            print(response.text)
            self.env['mailer.cloud.campaign'].search(
                [('campaign_id', '=', self.campaign_id)]).state = 'schedule'
        except:
            pass

    @api.constrains('schedule_date')
    def _check_schedule_date(self):
        if self.schedule_date <= fields.Datetime.today():
            raise ValidationError(
                "scheduled time should not be less than current date time")


class TestMail(models.TransientModel):
    _name = 'mailer.cloud.test.mail'

    email = fields.Char()
    campaign_id = fields.Char()

    @api.constrains('email')
    def check_email(self):
        print('function called......')
        match = re.match(
            '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
            self.email)
        if match == None:
            raise ValidationError('Not a valid E-mail ID')

    def action_send_mail(self):
        try:
            # api call to create test mail for campaign through mailer cloud
            url = "https://cloudapi.mailercloud.com/v1/campaign/testmail/" + self.campaign_id

            payload = json.dumps({
                "email": self.email
            })
            headers = {
                'Authorization': self.env['ir.config_parameter'].get_param(
                    'mailercloud_connector.api_key'),
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers,
                                        data=payload)

            print(response.text)
        except:
            pass
