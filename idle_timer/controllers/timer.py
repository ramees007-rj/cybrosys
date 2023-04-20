from odoo import http
from odoo.http import request
import time


class IdleTimer(http.Controller):
    @http.route('/time_idle', type='json',
                auth='public', website=True)
    def record_recently_viewed_e(self, **args):
        print(args['args']['token'])
        record = request.env['survey.survey'].search(
            [('access_token', '=', args['args']['token'])])
        print(record.read())
        return {
            'idle_time': record.idle_timer,
            'is_question_time_limit': record.is_question_time_limit,
            'question_time_limit': record.question_time_limit,
        }

        # records = request.env['survey.user_input'].sudo().search([],
        #                                                          order='id desc',
        #                                                          limit=1)
        # current_record = records.survey_id
        # section = 0
        # question = 0
        # number_of_pages = 0
        # for rec in current_record.question_and_page_ids:
        #     if not rec.question_type:
        #         section += 1
        #     else:
        #         question += 1
        # if current_record.questions_layout == 'one_page':
        #     number_of_pages = 1
        # elif current_record.questions_layout == 'page_per_section':
        #     number_of_pages = section
        # else:
        #     number_of_pages = question
        # print(records.state)
        #
        # values = {
        #     'idle_time': current_record.is_question_time_limit,
        #     'idle_time_limit': current_record.idle_timer,
        #     'idle_question_time_limit': current_record.question_time_limit,
        #     'number_of_pages': number_of_pages
        # }
        # print(values)
        # return values
