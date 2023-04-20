# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
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
#############################################################################
{
    'name': 'Fleet Live Location Lracker',
    'version': '16.0.1.0.0',
    'summary': 'Upload/Backup documents to google drive',
    'depends': ['fleet'],
    'category': 'Productivity',
    'author': 'Cybrosys Techno solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'data': [
        'views/fleet.xml',
        'templates/map_view.xml',
        'views/res_config.xml',
        'views/live_map.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'fleet_live_location_tracker/static/src/xml/live_location.xml',
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js',
            'fleet_live_location_tracker/static/src/js/live_location.js',
        ]
    },
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
