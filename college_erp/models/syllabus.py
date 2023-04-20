from odoo import models, fields


class Syllabus(models.Model):
    _name = 'syllabus'
    _description = 'Syllabus'

    name = fields.Char(string="Subject")
    course = fields.Many2one('college.course', string="Course")
    semester = fields.Many2one('college.semester', string="Semester")
    exam_id = fields.Many2one('college.exam')
    pass_mark = fields.Integer(string="Pass Mark")
    max_mark = fields.Integer(string="Maximum Mark")
