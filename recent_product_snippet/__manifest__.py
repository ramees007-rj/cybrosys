{
    'name': 'Recently Viewed Product',
    'version': '15.1.0.0',
    'category': 'Website',
    'sequence': -1,
    'summary': "You can select this product from edit section of website",
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'website',
        'web',
    ],
    'data': [
        'views/template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/recent_product_snippet/static/src/js/recent_product.js',
        ],
    },
}
