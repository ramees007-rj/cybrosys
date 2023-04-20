from odoo import models, fields, api


class CreateContactSurvey(models.Model):
    _name = "create.contact.survey"
    _description = "create contact from survey"

    survey_id = fields.Many2one('survey.survey')
    question_id = fields.Many2one("survey.question",
                                  string="Question")

    fields_id = fields.Many2one("ir.model.fields",
                                domain=[("model", "=", "res.partner")],
                                string='Customer')

    @api.onchange('fields_id')
    def sample_function(self):
        for rec in self.survey_id:
            return {
                'domain': {'question_id':
                               [('id', 'in',
                                 rec.question_and_page_ids.ids)]
                           }
            }


class CreateSurvey(models.Model):
    _inherit = 'survey.survey'

    contact_relation_ids = fields.One2many('create.contact.survey',
                                           'survey_id',
                                           string='Contact Relation')
