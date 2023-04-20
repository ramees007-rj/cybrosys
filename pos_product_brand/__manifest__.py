{
    'name': 'Product Brand POS',
    'version': '15.1.0.0',
    'category': 'Sales',
    'sequence': -1,
    'summary': "You can view the brand name under each sale order item",
    'description': '',
    'depends': [
        'sale', 'point_of_sale'
    ],
    'data': [
        'views/pos_brand.xml'
    ],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'pos_product_brand/static/src/JS/pos_brand_name.js'
        ],
        'web.assets_qweb': [
            'pos_product_brand/static/src/xml/pos_brand_name.xml'
        ],
    },
}
