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

from . import models
from . import controllers
from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(cr, registry):
    setup_provider(cr, registry, 'valitorpay')


def uninstall_hook(cr, registry):
    reset_payment_provider(cr, registry, 'valitorpay')
