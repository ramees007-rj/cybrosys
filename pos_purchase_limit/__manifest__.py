{
    'name': 'POS Purchase Limit',
    'version': '15.1.0.0',
    'category': 'Sales',
    'sequence': -1,
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'sale', 'point_of_sale'
    ],
    'data': [
        'views/purchase_limit.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_purchase_limit/static/src/js/customer_check.js'
        ],
        'web.assets_qweb': [
        ],
    },
}
