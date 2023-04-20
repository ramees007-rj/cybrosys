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

import logging
from odoo import http
from odoo.http import request
import braintree

_logger = logging.getLogger(__name__)


class BraintreeRedirect(http.Controller):
    @http.route('/payment/braintree/process_payment', type='json', auth='public')
    def braintree_process_payment(self, reference, payload, data):
        print("dddddddddd", data)
        print("UUUUUUUUUUU", payload)
        braintree_id = request.env['payment.acquirer'].sudo().browse(data['acquirer_id'])
        if braintree_id.sudo().state == 'enabled':
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment,
                merchant_id=braintree_id.sudo().merchant_id,
                public_key=braintree_id.sudo().public_key,
                private_key=braintree_id.sudo().private_key
            )
        )
        gateway.client_token.generate()
        partner = request.env['res.partner'].sudo().browse(data['partner_id'])
        transaction = gateway.transaction.sale({
            "amount": str(data['amount']),
            "order_id": data['reference'].split('-')[0],
            "payment_method_nonce": payload['nonce'],
            "customer": {
                "first_name": partner.sudo().name,
                "last_name": "",
                "email": partner.sudo().email,
                "phone": partner.sudo().phone
            },
            "options": {
                "submit_for_settlement": True
            },
        })
        print("Transaction..........",transaction)
        request.env['payment.transaction'].sudo()._handle_feedback_data('braintree', data)

    @http.route('/payment/braintree/get_token', type='json', auth='public')
    def braintree_get_token(self, acquirer_id):
        braintree_id = request.env['payment.acquirer'].sudo().search([('id', '=', acquirer_id)])
        if braintree_id.sudo().state == 'enabled':
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=environment,
                merchant_id=braintree_id.sudo().merchant_id,
                public_key=braintree_id.sudo().public_key,
                private_key=braintree_id.sudo().private_key,
            ))
        token = gateway.client_token.generate()
        return token
