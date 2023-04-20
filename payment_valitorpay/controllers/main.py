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
import pprint
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class ValitorpayPagoController(http.Controller):
    _return_url = '/payment/valitor/return'
    _webhook_url = '/payment/valitor/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['GET'])
    def valitorpay_return_from_checkout(self, **data):
        _logger.info("handling redirection from valitorpay with data:\n%s",
                     pprint.pformat(data))
        # Check the integrity of the notification
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data('valitorpay', data)
        # Handle the notification data
        tx_sudo._handle_notification_data('valitorpay', data)
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'],
                csrf=False)
    def valitorpay_webhook(self, **data):

        _logger.info("notification received from valitorpay with data:\n%s",
                     pprint.pformat(data))
        try:
            # Check the origin and integrity of the notification
            tx_sudo = request.env[
                'payment.transaction'].sudo()._get_tx_from_notification_data(
                'valitorpay', data
            )
            # Handle the notification data
            tx_sudo._handle_notification_data('valitorpay', data)
        except ValidationError:  # Acknowledge the notification to avoid getting spammed
            _logger.exception(
                "unable to handle the notification data; skipping to acknowledge")

        return 'SUCCESS'  # Acknowledge the notification
