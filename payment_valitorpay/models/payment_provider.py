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

from odoo import fields, models, api, _
from odoo.http import request


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('valitorpay', "Valitor Pay")],
        ondelete={'valitorpay': 'set default'})
    merchant_id = fields.Char(
        string="Merchant ID",
        help="Merchant ID of Valitor Pay")
    verification_code = fields.Char(
        string="Verification Code",
        help="Verification Code")

    def get_base_url(self):
        if request and request.httprequest.url_root:
            return request.httprequest.url_root
        return super().get_base_url()
