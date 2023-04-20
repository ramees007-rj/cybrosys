# -*- coding: utf-8 -*-
########################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
##########################################################################################

from odoo import fields, api, models, SUPERUSER_ID


class ThemeConfig(models.Model):
    """ Theme Config for night mode"""
    _inherit = "res.users"

    check = fields.Boolean(string="Active", default='false',
                           help="Enable / Disable checkbox")

    @api.model
    def set_active(self):
        """ Activate checkbox.
                :param : model
                :return :  value of checkbox """
        if self.env['res.users'].sudo().browse(SUPERUSER_ID):
            user_obj = self.env['res.users'].sudo().browse(SUPERUSER_ID)
            user_obj.check = True

        else:
            user_obj = self.env['res.users'].search(
                [('id', '=', self.env.user.id)])
            user_obj.write({'check': True})
            user_obj.check = True
        return user_obj.check

    @api.model
    def set_deactive(self):
        """ Deactivate checkbox.
                        :param : model
                        :return : value of checkbox """
        if self.env['res.users'].sudo().browse(SUPERUSER_ID):
            user_obj = self.env['res.users'].sudo().browse(SUPERUSER_ID)
            user_obj.check = False
        else:
            user_obj = self.env['res.users'].search(
                [('id', '=', self.env.user.id)])
            user_obj.check = False
        return user_obj.check

    @api.model
    def create(self, values):
        """ Create .
                    :param : model
                    :param : values
                       """
        result = super(ThemeConfig, self).create(values)
        return result

    # @api.multi
    def write(self, values):
        """ Write .
                    :param : model
                    :param : values
                """
        result = super(ThemeConfig, self).write(values)
        return result

    @api.model
    def get_active(self):
        """ Get value of checkbox.
                        :param : model
                        :return :  value of checkbox """
        if self.env['res.users'].sudo().browse(SUPERUSER_ID):
            result = self.env['res.users'].sudo().browse(SUPERUSER_ID)
            return result.check
        else:
            return self.env['res.users'].search(
                [('id', '=', self.env.user.id)]).check
