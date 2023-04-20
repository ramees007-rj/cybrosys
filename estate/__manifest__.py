{
    'name': 'estate',
    'version': '15.1.0.0',
    'category': 'estate',
    'sequence': -15,
    'application': True,
    'summary': "it's all about estate",
    'description': '',
    'installable': True,
    'depends': [
        'sale'

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property.xml',

    ],
    'demo': [],
    'auto_install': False,

}
