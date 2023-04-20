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
{
    'name': 'Braintree Payment Gateway Integration',
    'version': '15.0.1.0.0',
    'summary': 'Braintree Payment Acquirer',
    'description': 'Braintree Payment Acquirer',
    'category': 'Accounting/Payment Acquirers',
    'author': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['payment'],
    'data': [
        'views/payment_braintree_template.xml',
        'views/braintree.xml',
        'data/data.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'external_dependencies': {
        'python': ['braintree'],
    },
    'assets': {
        'web.assets_frontend': [
            'braintree_payment_gateway/static/src/js/payment_form.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 49,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,

}
