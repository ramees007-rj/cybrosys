# -*- coding: utf-8 -*-
##############################################################################
#
#    Boðleið ehf.
#
#    Copyright (C) 2022-TODAY Boðleið ehf.(<https://bodleid.is/>).
#    Author: Boðleið ehf.(<https://bodleid.is/>)
#    you can modify it under the terms of the GNU OPL (v1), Version 1.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU OPL (OPL v1) for more details.
#
##############################################################################

import logging
from hashlib import sha256
from odoo.exceptions import ValidationError
from odoo import _, api, models, fields

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    sale_reference = fields.Char()

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'valitorpay':
            return res
        else:
            transaction_id = self.env['payment.transaction'].sudo().search(
                [('reference', '=', processing_values['reference'])])
            provider_id = self.env['payment.provider'].sudo().search(
                [('code', '=', 'valitorpay')])
            sale_order = transaction_id.sale_order_ids
            currency_id = self.env['res.currency'].sudo().search(
                [('id', '=', processing_values['currency_id'])])
            # currency = currency_id.name
            currency = "ISK"
            base_url = self.provider_id.get_base_url()
            merchant_id = provider_id.merchant_id
            verification_code = provider_id.verification_code
            if provider_id.state == 'test':
                base_url_valitor = 'https://paymentweb.uat.valitor.is/?AuthorizationOnly=0&'
            if provider_id.state == 'enabled':
                base_url_valitor = 'https://paymentweb.valitor.is/?AuthorizationOnly=0&'
            list = []
            signature_list = []
            reference = processing_values['reference']
            self.sale_reference = reference
            new_url = ''
            for i in range(len(sale_order.order_line)):
                product = sale_order.order_line[i].product_id.name
                description = str(product).replace(" ", "%20")
                quantity = int(sale_order.order_line[i].product_uom_qty)
                price = sale_order.order_line[i].price_unit
                discount = round((sale_order.order_line[i].price_unit * sale_order.order_line[i].discount) / 100, 2)
                qty = i + 1
                product_url = "Product_" + str(
                    qty) + "_Description=" + description + "&" + "Product_" + str(
                    qty) + "_Quantity=" + str(
                    quantity) + "&" + "Product_" + str(
                    qty) + "_Price=" + str(
                    price) + "&" + "Product_" + str(
                    qty) + "_Discount=" + str(discount) + "&"
                list.append(product_url)
            return_url = base_url + 'payment/valitor/return'
            return_text = 'Return'
            merchant_url = "MerchantID=" + str(merchant_id) + "&"
            reference_url = "ReferenceNumber=" + str(
                processing_values['reference']) + "&"
            successful_url = "PaymentSuccessfulURL" + return_url + "&"
            url_text = "PaymentSuccessfulURLText" + "Return" + "&"
            currency_url = "Currency=" + currency + "&"
            list.append(merchant_url)
            list.append(reference_url)
            list.append(successful_url)
            list.append(url_text)
            list.append('PaymentSuccessfulAutomaticRedirect=1&')
            list.append(currency_url)
            #     For generating Digital signature
            signature_list.append(verification_code)
            signature_list.append('0')
            for i in range(len(sale_order.order_line)):
                quantity = int(sale_order.order_line[i].product_uom_qty)
                price = sale_order.order_line[i].price_unit
                discount = round((sale_order.order_line[i].price_unit * sale_order.order_line[i].discount) / 100, 2)
                signature = str(quantity) + str(price) + str(discount)
                signature_list.append(signature)
            signature_list.append(str(merchant_id))
            signature_list.append(processing_values['reference'])
            signature_list.append(return_url)
            signature_list.append(currency)
            signature_string = ''
            for i in signature_list:
                signature_string = signature_string + i
            # Generating SHA256 hash
            hash_result = sha256(str(signature_string).encode())
            result = hash_result.hexdigest()
            # Printing the result
            digital_sign = "DigitalSignature=" + result
            list.append(digital_sign)
            for i in list:
                new_url = new_url + i
            api_url = base_url_valitor + new_url
            rendering_values = {
                'api_url': api_url,
                'return_url': return_url,
                'return_text': return_text,
            }
            return rendering_values

    def _get_tx_from_notification_data(self, provider_code, notification_data):

        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'valitorpay' or len(tx) == 1:
            return tx
        reference = notification_data.get('ReferenceNumber')
        tx = self.search([('reference', '=', reference),
                          ('provider_code', '=', 'valitorpay')])
        if not tx:
            raise ValidationError(
                "Valitor Pay: " + _(
                    "No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'valitorpay':
            return
        if notification_data.get(
                'DigitalSignatureResponse') == self.compute_expected_signature():
            self._set_done()
        else:
            self._set_error(
                "Valitor Pay: " + _("received invalid transaction status:"))

    def compute_expected_signature(self):
        provider_id = self.env['payment.provider'].sudo().search(
            [('code', '=', 'valitorpay')])
        reference = self.sale_reference
        signature_string = provider_id.verification_code + self.sale_reference
        # Generating SHA256 hash
        hash_result = sha256(str(signature_string).encode())
        result = hash_result.hexdigest()
        return result
