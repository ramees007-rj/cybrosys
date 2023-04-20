{
    'name': 'POS Product Rating',
    'version': '15.1.0.0',
    'category': 'Sales',
    'sequence': -1,
    'summary': "You can see product rating in order and receipt",
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'sale', 'point_of_sale'
    ],
    'data': [
        'views/product_rating.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_product_rating/static/src/js/product_rating.js'
        ],
        'web.assets_qweb': [
            'pos_product_rating/static/src/xml/product_rating.xml'
        ],
    },
}
