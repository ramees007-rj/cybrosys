# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
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
########################################################################################

{
    "name": "Night Mode",
    "summary": "Odoo 14 Night mode Dark Theme",
    "version": "15.0.1.0.0",
    "category": "Theme/Backend",
    "website": "https://www.cybrosys.com",
    "description": """
        Odoo Night mode backend dark theme for Odoo 14 Community Version, odoo 14, odoo14, theme, backend theme,odoo14 theme,
    """,
    'images': ['static/description/banner.png',
               'static/description/theme_screenshot.png'
               ],
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    "data": [
    ],
    'depends': ['base'],
    'assets': {
        'web.assets_backend': [
            '/night_mode_odoo/static/src/scss/theme_style_backend.scss',
            '/night_mode_odoo/static/src/js/systray_theme_menu.js',
        ],
        'web.assets_qweb': [
            '/night_mode_odoo/static/src/xml/systray_ext.xml',
        ],
    },
    'license': 'OPL-1',
    'price': 29.99,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
}
