{
    'name': 'POS Product Available Quantity',
    'version': '15.1.0.0',
    'category': 'Sales',
    'sequence': -1,
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'point_of_sale', 'product'
    ],
    'data': [
        'views/location_configuration.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'product_available_quantity_pos/static/src/js/available_quantity.js'
        ],
        'web.assets_qweb': [
            'product_available_quantity_pos/static/src/xml/available_quantity.xml'
        ],
    },
}
