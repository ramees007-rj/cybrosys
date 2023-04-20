# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ramees Jaman KT (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
{
    'name': "Web Responsive",
    'version': '16.0.1.0.0',
    'summary': 'This module adds responsiveness to web backend',
    'description': """This module adds responsiveness to web backend""",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    "depends": ["base", "web", "mail"],
    "assets": {
        "web.assets_backend": [
            '/web_responsive/static/src/css/main.css',
            '/web_responsive/static/src/components/apps_menu/menu_order.css',
            '/web_responsive/static/src/components/apps_menu/link_view.xml',
            '/web_responsive/static/src/components/apps_menu/apps_menu.js',
            '/web_responsive/static/templates/side_bar.xml',
            '/web_responsive/static/src/xml/PivotCustom.xml'
        ]
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}