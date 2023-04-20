from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class InheritSurveyInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    value_many2one_box = fields.Integer('Free Many2one answer')
    value_selection_field = fields.Char('Selection field answer')
    answer_type = fields.Selection([
        ('text_box', 'Free Text'),
        ('char_box', 'Text'),
        ('numerical_box', 'Number'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('Many2one', 'Many2one Selection'),
        ('selection', 'Selection'),
        ('suggestion', 'Suggestion')], string='Answer Type')

    @api.constrains('skipped', 'answer_type')
    def _check_answer_type_skipped(self):
        for line in self:
            if (line.skipped == bool(line.answer_type)):
                raise ValidationError(
                    _('A question can either be skipped or answered, not both.'))

            # allow 0 for numerical box
            if line.answer_type == 'numerical_box' and float_is_zero(
                    line['value_numerical_box'], precision_digits=6):
                continue
            if line.answer_type == 'suggestion':
                field_name = 'suggested_answer_id'
            elif line.answer_type == 'Many2one':
                field_name = 'value_many2one_box'
            elif line.answer_type == 'selection':
                field_name = 'value_selection_field'
            elif line.answer_type:
                field_name = 'value_%s' % line.answer_type
            else:  # skipped
                field_name = False
            if field_name and not line[field_name]:
                raise ValidationError(
                    _('The answer must be in the right type'))


class InheritSurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_type = fields.Selection([
        ('simple_choice', 'Multiple choice: only one answer'),
        ('multiple_choice', 'Multiple choice: multiple answers allowed'),
        ('text_box', 'Multiple Lines Text Box'),
        ('char_box', 'Single Line Text Box'),
        ('numerical_box', 'Numerical Value'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('matrix', 'Matrix'),
        ('Many2one', 'Many2one Selection'),
        ('selection', 'Selection')], string='Question Type',
        compute='_compute_question_type', readonly=False, store=True)
    model_name = fields.Many2one('ir.model', string='Model Name')
    selection_items_ids = fields.One2many('survey.selection', 'question_id',
                                          string='Selection Items')

    # column_line_ids = fields.One2many('')

    def get_model_values(self):
        record = self.env[self.model_name.model].search([])
        return record

    def get_selection_values(self):
        return self.selection_items_ids


class InheritSurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    partner_id_check = fields.Boolean()

    def save_lines(self, question, answer, comment=None):
        """ Save answers to questions, depending on question type

            If an answer already exists for question and user_input_id, it will be
            overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])

        if question.question_type in ['char_box', 'text_box', 'numerical_box',
                                      'date', 'datetime']:
            self._save_line_simple_answer(question, old_answers, answer)
            if question.save_as_email and answer:
                self.write({'email': answer})
            if question.save_as_nickname and answer:
                self.write({'nickname': answer})

        elif question.question_type in ['simple_choice', 'multiple_choice']:
            self._save_line_choice(question, old_answers, answer, comment)
        elif question.question_type == 'matrix':
            self._save_line_matrix(question, old_answers, answer, comment)
        elif question.question_type == 'Many2one':
            self._save_line_selection_answer(question, old_answers, answer)
        elif question.question_type == 'selection':
            self._save_line_select_answer(question, old_answers, answer)
        else:
            raise AttributeError(
                question.question_type + ": This type of question has no saving function")

    def _save_line_selection_answer(self, question, old_answers, answer):
        vals = self._get_line_answer_values(question, answer,
                                            question.question_type)
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env['survey.user_input.line'].create(vals)

    def _save_line_select_answer(self, question, old_answers, answer):
        vals = self._get_line_answer_values(question, answer,
                                            question.question_type)
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env['survey.user_input.line'].create(vals)

    def _get_line_answer_values(self, question, answer, answer_type):
        vals = {
            'user_input_id': self.id,
            'question_id': question.id,
            'skipped': False,
            'answer_type': answer_type,
        }
        if not answer or (isinstance(answer, str) and not answer.strip()):
            vals.update(answer_type=None, skipped=True)
            return vals

        if answer_type == 'suggestion':
            vals['suggested_answer_id'] = int(answer)
        elif answer_type == 'numerical_box':
            vals['value_numerical_box'] = float(answer)
        elif answer_type == 'Many2one':
            vals['value_many2one_box'] = int(answer)
        elif answer_type == 'selection':
            vals['value_selection_field'] = answer
        else:
            vals['value_%s' % answer_type] = answer
        return vals


class SurveySelectionQuestion(models.Model):
    _name = 'survey.selection'

    name = fields.Char(string='name')
    question_id = fields.Many2one('survey.question')


# class SurveyOne2manyColumn(models.Model):
#     _name = 'survey.one2many.column'
#
#     name = fields.Char(string='Name')
