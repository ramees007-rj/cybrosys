{
    'name': 'POS Conf',
    'version': '16.1.0.0',
    'category': 'Sales',
    'sequence': -1,
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'point_of_sale', 'web', 'base'
    ],
    'data': [
        'views/suggestion_product.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_configuration/static/src/js/suggestion_product.js',
            'pos_configuration/static/src/xml/CustomerFacingDisplay/CustomerFacingDisplay.xml'
        ]
    },
    'application': True,
    'installable': True,
}
