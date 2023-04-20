{
    'name': 'POS Credit Limit',
    'version': '16.1.0.0',
    'category': 'Sales',
    'sequence': -1,
    'summary': "You can set credit limit for your customer",
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'account','point_of_sale'
    ],
    'data': [
        'views/credit_journal.xml',
        'views/partner_credit_limit.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'POS_credit_limit/static/src/js/partner_limit.js',
            'POS_credit_limit/static/src/xml/partner_view.xml'
        ]
    },
    'application': True,
    'installable': True,

}
