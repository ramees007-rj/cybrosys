{
    'name': 'Import Order Line',
    'version': '15.1.0.0',
    'category': 'Sales',
    'sequence': -15,
    'summary': "You can import sale order lines",
    'application': True,
    'sequence': -1,
    'description': '',
    'installable': True,
    'depends': [
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/import_button.xml',
    ],
}
