{
    'name': 'Payslip Portal',
    'version': '15.1.0.0',
    'category': 'Website',
    'sequence': -1,
    'summary': "You can select payslip from my account website",
    'application': True,
    'description': '',
    'installable': True,
    'depends': [
        'portal', 'hr_payroll_community', 'website', 'hr'
    ],
    'data': [
        'views/payslip_portal.xml',
        'views/report_template.xml',
    ],
}
