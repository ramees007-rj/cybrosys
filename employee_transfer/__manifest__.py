{
    'name': 'Employee Transfer',
    'version': '15.1.0.0',
    'category': 'Employee',
    'sequence': -2,
    'summary': 'Employee transfer',
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'hr', 'base'
    ],
    'data': [
        'security/transfer_security.xml',
        'security/ir.model.access.csv',
        'views/employee_transfer_request.xml',
        'views/transfer_portal.xml',
    ],
}
