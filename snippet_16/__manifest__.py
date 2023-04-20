{
    'name': 'Dynamic Snippet',
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
        'views/snippet.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            '/snippet_16/static/src/js/snippet.js'
        ],
    },
}
