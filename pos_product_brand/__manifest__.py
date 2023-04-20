# -*- coding: utf-8 -*-
{
    'name': "POS Product Brand",

    'summary': """
        Adds a new field for product brand""",

    'description': """
        Description
    """,

    'author': "Minions 6",

    'version': '15.0.1.0.0',
    'depends': ['point_of_sale'],

    'data': [
        'views/product_brand_inherits.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            # 'pos_product_brand/static/src/xml/pos_product_brand.xml',
        ],
        'web.assets_backend': [
            # 'pos_product_brand/static/src/js/brand.js',
        ]
    }
}
