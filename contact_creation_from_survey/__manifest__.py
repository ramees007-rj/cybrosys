{
    'name': "Contact Creation from survey",
    'version': "15.0.1.1",
    'sequence': -50,
    'depends': ['survey', 'base'],
    'description': "Contact Creation from survey",
    'data': [
        'security/ir.model.access.csv',
        'views/create_contact_from_survey.xml',
    ],
    'assets':
        {
            'web.assets_frontend': [
                'contact_creation_from_survey/static/src/js/contact_creation.js']},

    'demo': [],
    'application': True,
    'installable': True,
    'auto install': False,
    'license': 'LGPL-3',
}
