from odoo import models, fields, api


class CollegeMarkSheet(models.Model):
    _name = 'college.mark.sheet'
    _description = 'College Mark Sheet'
    _rec_name = 'student_id'

    student_id = fields.Many2one('college.students', string='Student')
    exam = fields.Many2one('college.exam', string='Exam')
    class_name = fields.Many2one('college.class', string='Class')
    course = fields.Char(related='class_name.course_id.name', string='Course')
    semester = fields.Integer(
        related='class_name.semester_id.number_of_semester',
        string='semester', store=True)
    pass_or_fail = fields.Boolean(string='Pass/Fail',
                                  compute='_compute_pass_or_fail', store=True)
    mark_sheet_id = fields.Char()
    subject_ids = fields.One2many('college.student.subject', 'exam_id')
    total_mark = fields.Integer(string="Total Mark",
                                compute='_compute_total_mark', store=True)

    @api.depends('subject_ids')
    def _compute_total_mark(self):
        for rec in self:
            print(sum(rec.subject_ids.mapped('mark')))
            rec.total_mark = sum(rec.subject_ids.mapped('mark'))

    @api.depends('subject_ids.pass_mark')
    def _compute_pass_or_fail(self):
        for rec in self:
            for reco in rec.subject_ids:
                # total = sum(rec.subject_ids.mapped('pass_mark'))
                # print(total, "ss")
                if not reco.pass_or_fail:
                    rec.pass_or_fail = False
                    break
                else:
                    rec.pass_or_fail = True
