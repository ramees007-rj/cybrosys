{
    'name': 'Cloud Cluster Import',
    'depends': ['base', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config.xml',
        'views/cloud_cluster_machine_analysis.xml'
    ]
}
