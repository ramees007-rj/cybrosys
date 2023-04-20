from odoo import http
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request


class SurveySubmit(Survey):
    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>',
                type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        print("function called")
        res = super(SurveySubmit, self).survey_submit(survey_token,
                                                      answer_token)
        question_dict = {}
        survey_id = request.env['survey.survey'].sudo().search([])
        for rec in post:
            for survey in survey_id.contact_relation_ids:
                if rec == str(survey.question_id.id):
                    question_dict.update({survey.fields_id.name: post[rec]})
        request.env['res.partner'].create(question_dict)
        return res