{
    'name': 'College ERP',
    'version': '15.0,1.0.0',
    'category': 'college',
    'sequence': -2,
    'application': True,
    'summary': "it's all about ",
    'description': '',
    'installable': True,
    'depends': [
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/student.xml',
        'data/email_template.xml',
        'data/mail_template_lost.xml',
        'data/application_no.xml',
        'data/admission_no.xml',
        'data/mark_sheet_no.xml',
        'data/exam_state_change.xml',
        'views/semester.xml',
        'views/class.xml',
        'views/exam.xml',
        'views/syllabus.xml',
        'views/mark_sheet.xml',
        'views/student_subject.xml',
        'views/promotion.xml',
        'report/mark_sheet_report.xml',
        'report/mark_sheet_report_template_stdnt.xml',
        'report/mark_sheet_report_template_class.xml',
    ],
    'assets': {'web.assets_backend': [
        'college_erp/static/src/js/action_manager.js', ]
    }

    ,
    'demo': [],
    'auto_install': False,

}
