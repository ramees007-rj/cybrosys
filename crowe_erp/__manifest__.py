{
    'name': 'Crowe ERP',
    'version': '16.0.1.1.1',
    'depends': ['base', 'sale_management', 'sale_project', 'project',
                'account', 'hr', 'sale_timesheet', 'survey',
                'crowe_base_accounting_kit', 'hr_payroll_community'],
    'data': [
        'security/crowe_security.xml',
        'security/ir.model.access.csv',
        'data/work_order_template.xml',
        'data/crowe_data.xml',
        'data/letter_of_engagement.xml',
        'data/loe_email_template.xml',
        'data/crowe_category.xml',
        'data/project_data.xml',
        'data/custom_report_template.xml',
        'data/cost_sheet_template.xml',
        'data/invoice_template_re.xml',
        'data/crowe_contract_structure.xml',
        'views/sales_configuration.xml',
        'views/cost_sheet_view.xml',
        'views/project_form_view.xml',
        'views/project_task_view1.xml',
        'views/account_configuration.xml',
        'views/work_order_view.xml',
        'views/survey.xml',
        'views/hr_inherit.xml',
        'views/report_crowe.xml',
        'views/product_template.xml',
        'views/res_company_view.xml',
        'views/contract_inherit.xml',
        'views/payroll_inherit.xml',
        'views/access_right_modification.xml',
        'report/project_report.xml'
    ],
    'assets': {
        'survey.survey_assets': [
            'crowe_erp/static/src/js/survey_form_extension.js',
            'crowe_erp/static/src/scss/survey_select.scss'
        ],
        'web.assets_backend': [
            'crowe_erp/static/src/js/action_manager.js'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
