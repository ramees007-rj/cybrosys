{
    'name': 'CRM Dashboard',
    'version': '15.1.0.0',
    'category': 'CRM',
    'sequence': -1,
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'sale',
        'crm',
    ],
    'data': [
        'views/stage_in_srm_team.xml',
        'views/dashboard.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'crm_dashboard/static/src/js/dashboard_menu.js'
        ],
        'web.assets_qweb': [
            'crm_dashboard/static/src/xml/dashboard_view.xml'
        ],
    },
}
