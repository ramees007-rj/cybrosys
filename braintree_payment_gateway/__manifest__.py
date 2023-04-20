{
    'name': 'Braintree Payment Gateway Integration',
    'depends': ['payment', 'account'],
    'data': [
        'views/braintree_template.xml',
        'views/braintree.xml',
        'data/data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'braintree_payment_gateway/static/src/js/payment_form.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',

}
