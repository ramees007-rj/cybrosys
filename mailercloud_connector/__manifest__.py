{
    'name': 'Mailer Cloud Connector',
    'version': '16.0.0.0.0',
    'category': 'Email Marketing',
    'sequence': -10,
    'summary': '',
    'depends': ['base', 'account', 'mass_mailing', 'sale', 'purchase'],
    'data': [
        'security/res_group_data.xml',
        'security/ir.model.access.csv',
        'views/campaign_regular.xml',
        'views/audience_list.xml',
        'views/settings_view.xml',
        'views/contact.xml',
        'views/fetch_data.xml',
        'views/audience_segment.xml',
    ],
    'application': True
}
