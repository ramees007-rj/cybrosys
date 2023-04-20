from odoo import http
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request

partner = None
questionnaire = None


class SurveySubmit(Survey):
    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>',
                type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        print(post)
        # todo
        #  address,location,Nature of entity,If other industry, kindly specify,Year and Date of company registration,Registered capital,invested capital
        # page 1
        if survey_token == request.env.ref(
                'crowe_erp.crowe_questionnaire_survey').access_token:
            if post['page_id'] == str(request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question_p1').id):
                global partner
                global questionnaire
                if int(post[str(request.env.ref(
                        'crowe_erp.crowe_questionnaire_survey_question1').id)]) == request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question1_c1').id and int(
                    post[str(request.env.ref(
                        'crowe_erp.crowe_questionnaire_survey_question2').id)]) == request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question2_c1').id:
                    request.env['survey.user_input'].search(
                        [('access_token', '=', answer_token)]).write({
                        'partner_id_check': True
                    })
                    questionnaire = post[str(request.env.ref(
                        'crowe_erp.crowe_questionnaire_survey_question4').id)]
                return super(SurveySubmit, self).survey_submit(survey_token,
                                                               answer_token,
                                                               **post)
            # page 2
            elif post['page_id'] == str(request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question_p2').id):
                print("function_page_2 called.")
                print(questionnaire)
                if request.env['survey.user_input'].search(
                        [('access_token', '=', answer_token)]).partner_id_check:
                    data_dict = {}
                    for rec in post:
                        if rec == str(request.env.ref('crowe_erp.crowe_questionnaire_survey_question5').id):
                            data_dict['name'] = post[rec]
                        print(request.env['questionnaire'].browse(questionnaire))
                        request.env['questionnaire'].browse(
                            int(questionnaire)).partner_id.write(data_dict)
                        partner = request.env['questionnaire'].browse(
                            int(questionnaire)).partner_id
                    return super(SurveySubmit, self).survey_submit(
                        survey_token,
                        answer_token,
                        **post)
                else:
                    data_dict = {}
                    for rec in post:
                        if rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question5').id):
                            data_dict['name'] = post[rec]
                    data_dict['is_company'] = True
                    partner = request.env['res.partner'].create(data_dict)
                    questionnaire_id = request.env['questionnaire'].create({
                        'partner_id': partner.id
                    })
                    questionnaire = questionnaire_id.id
                    return super(SurveySubmit, self).survey_submit(
                        survey_token,
                        answer_token,
                        **post)
                # page 3
            elif post['page_id'] == str(request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question_p3').id):
                print("............")
                data_dict = {}
                for rec in post:
                    if rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question6').id):
                        data_dict['street'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question7').id):
                        data_dict['street2'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question8').id):
                        data_dict['city'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question9').id):
                        print(post[rec])
                        data_dict['country_id'] = int(post[rec])
                request.env['res.partner'].browse(partner.id).write(data_dict)
                return super(SurveySubmit, self).survey_submit(
                    survey_token,
                    answer_token,
                    **post)

                # page 4
            elif post['page_id'] == str(request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question_p4').id):
                print("llllll")
                data_dict = {}
                for rec in post:
                    if rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question30').id):
                        data_dict['phone'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question41').id):
                        data_dict['mobile'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question31').id):
                        data_dict['vat'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question32').id):
                        data_dict['email'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question33').id):
                        data_dict['website'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question36').id):
                        data_dict['industry_id'] = int(post[rec])
                request.env['res.partner'].browse(partner.id).write(data_dict)
                return super(SurveySubmit, self).survey_submit(
                    survey_token,
                    answer_token,
                    **post)

            elif post['page_id'] == str(request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question_p5').id):
                if request.env['survey.user_input'].search(
                        [('access_token', '=',
                          answer_token)]).partner_id_check:
                    data_dict = {}
                    for rec in post:
                        if rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question50').id):
                            data_dict['name'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question51').id):
                            data_dict['function'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question52').id):
                            data_dict['email'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question53').id):
                            data_dict['phone'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question54').id):
                            data_dict['mobile'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question55').id):
                            data_dict['comment'] = post[rec]

                    data_dict['parent_id'] = partner.id
                    request.env['res.partner'].browse(
                        request.env['res.partner'].browse(
                            partner.id).child_ids.id).write(data_dict)
                    return super(SurveySubmit, self).survey_submit(
                        survey_token,
                        answer_token,
                        **post)

                else:
                    data_dict = {}
                    for rec in post:
                        if rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question50').id):
                            data_dict['name'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question51').id):
                            data_dict['function'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question52').id):
                            data_dict['email'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question53').id):
                            data_dict['phone'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question54').id):
                            data_dict['mobile'] = post[rec]
                        elif rec == str(request.env.ref(
                                'crowe_erp.crowe_questionnaire_survey_question54').id):
                            data_dict['comment'] = post[rec]
                    data_dict['parent_id'] = partner.id
                    request.env['res.partner'].create(data_dict)
                    return super(SurveySubmit, self).survey_submit(
                        survey_token,
                        answer_token,
                        **post)
            elif post['page_id'] == str(request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question_p6').id):
                for rec in post:
                    if rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question61').id):
                        date_from = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question62').id):
                        date_to = post[rec]
                request.env['questionnaire'].browse(
                    questionnaire).write(
                    {'accounting_period': date_from + ' to ' + date_to})
                return super(SurveySubmit, self).survey_submit(
                    survey_token,
                    answer_token,
                    **post)
            elif post['page_id'] == str(request.env.ref(
                    'crowe_erp.crowe_questionnaire_survey_question_p7').id):
                data_dict = {}
                for rec in post:
                    print(rec)
                    print(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question72').id)
                    if rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question71').id):
                        data_dict['constitution'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question72').id):
                        data_dict['comm_reg_no'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question73').id):
                        data_dict['reg_capital'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question74').id):
                        data_dict['members'] = post[rec]
                    elif rec == str(request.env.ref(
                            'crowe_erp.crowe_questionnaire_survey_question75').id):
                        data_dict['main_activities'] = post[rec]
                    print(data_dict)
                    request.env['questionnaire'].browse(
                        questionnaire).write(data_dict)
                return super(SurveySubmit, self).survey_submit(
                    survey_token,
                    answer_token,
                    **post)
            else:
                return super(SurveySubmit, self).survey_submit(
                    survey_token,
                    answer_token,
                    **post)
        else:
            return super(SurveySubmit, self).survey_submit(
                survey_token,
                answer_token,
                **post)
        # def new_customer(self, answer_token, post):
        #
        #
        # def old_customer(self):
        #     print('function old_customer..............')
