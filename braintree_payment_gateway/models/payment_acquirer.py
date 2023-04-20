# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Arunima (odoo@cybrosys.com)
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
#############################################################################

from odoo import models, fields, api, _
import braintree
from odoo.exceptions import ValidationError


class BraintreePaymentGateway(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('braintree', 'Braintree')],
        ondelete={'braintree': 'set '
                               'default'})
    merchant_id = fields.Char('Merchant ID')
    public_key = fields.Char('Public Key')
    private_key = fields.Char('Private Key')

    def write(self, vals):
        res = super(BraintreePaymentGateway, self).write(vals)
        if self.provider != 'braintree':
            return res
        if self.state == 'enabled':
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox

        if self.merchant_id and self.private_key and self.public_key:
            try:
                gateway = braintree.BraintreeGateway(
                    braintree.Configuration(
                        environment=environment,
                        merchant_id=self.merchant_id,
                        public_key=self.public_key,
                        private_key=self.private_key,
                    ))
                token = gateway.client_token.generate()
            except:
                raise ValidationError(_('Invalid Credentials!'))

        return res

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'braintree':
            return super()._get_default_payment_method_id()
        return self.env.ref('braintree_payment_gateway.payment_method_braintree').id


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['braintree'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res
