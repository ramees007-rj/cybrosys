{
    'name': 'Quiz - Idle timer',
    'version': '15.1.0.0',
    'sequence': -1,
    'summery': "You can set timer for your Quiz",
    'application': True,
    'installable': True,
    'depends': [
        'survey','web'
    ],
    'data': [
        'views/time_configuration.xml'
    ],
    'assets': {
        'survey.survey_assets': [
            'idle_timer/static/src/js/idle_timer.js',
        ],
    },
}
