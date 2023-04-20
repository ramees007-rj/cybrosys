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

{
    'name': 'Valitor Pay ',
    'category': 'Accounting/Payment Acquirers',
    'version': '16.0.1.1.4',
    'description': """Valitor Pay Payment""",
    'author': "Boðleið ehf.",
    'website': "https://bodleid.is/",
    'company': 'Boðleið ehf.',
    'maintainer': 'Boðleið ehf.',
    'license': 'OPL-1',
    'depends': ['payment'],
    'data': [
        # 'views/payment_provider_views.xml',
        # 'views/payment_template.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': True,
    'auto_install': False,

}
