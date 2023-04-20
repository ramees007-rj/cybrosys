{
    'name': 'Discount Approval',
    'version': '15.1.0.0',
    'category': 'Sales',
    'sequence': -15,
    'summary': "setting discount limit",
    'application': True,
    'sequence': -1,
    'description': '',
    'installable': True,
    'depends': [
        'sale',
        'base',
        'resource',
    ],
    'data': [
        'security/discount_security.xml',
        'security/ir.model.access.csv',
        'views/discount_limit.xml'

    ],
}
