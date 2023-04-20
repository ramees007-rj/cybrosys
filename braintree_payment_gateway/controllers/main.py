import logging
from odoo import http
from odoo.http import request
import braintree

_logger = logging.getLogger(__name__)


class BraintreeRedirect(http.Controller):
    @http.route('/payment/braintree/get_token', type='json', auth='public')
    def braintree_get_token(self, acquirer_id):
        braintree_id = request.env['payment.provider'].sudo().search([('id', '=', acquirer_id)])
        if braintree_id.sudo().state == 'enabled':
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=environment,
                merchant_id='wvn354htkf6wbhcv',
                public_key='n992z4xpcvc4pxtk',
                private_key='9e5a850e05996214799373f942e912e2'
            ))
        token = gateway.client_token.generate()
        return token

    @http.route('/payment/braintree/process_payment', type='json', auth='public')
    def braintree_process_payment(self, reference, payload, data):
        print(payload)
        braintree_id = request.env['payment.provider'].sudo().browse(data['provider_id'])
        if braintree_id.sudo().state == 'enabled':
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment,
                merchant_id='wvn354htkf6wbhcv',
                public_key='n992z4xpcvc4pxtk',
                private_key='9e5a850e05996214799373f942e912e2'
            )
        )
        print("gateway", gateway)
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
        print("Transaction", transaction)
        print("::::::::::::::::::",data)
        transaction = request.env['payment.transaction'].sudo()._handle_notification_data('braintree', data)
        print("dddddddddddddd",transaction)
