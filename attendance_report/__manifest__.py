{
    'name': 'Attendance Report',
    'version': '15.0.1.0.0',
    'category': 'Daily Attendance Report',
    'sequence': -93,
    'application': True,
    'license': 'LGPL-3',
    'depends': ['base', 'hr', 'report_xlsx'],
    'data': [
        'data/attendance_scheduler.xml',
        'report/report_action.xml',
        'report/report_template.xml',
    ],
}
