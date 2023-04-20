from odoo import models, fields, api


class CollegeClassPromotion(models.Model):
    _name = 'college.class.promotion'
    _description = 'College Class Promotion'
    _rec_name = 'exam_id'

    exam_id = fields.Many2one('college.exam', string='Exam')
    class_id = fields.Many2one('college.class', string='Class')
    semester = fields.Char(string='Semester',
                           related='class_id.semester_id.name')
    course = fields.Char(string='Course', related='class_id.course_id.name')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ], string='Status', required=True, readonly=True, copy=False,
        default='pending')
    qualified_student_ids = fields.One2many('college.students',
                                            'promotion_class')
    gp_button_count = fields.Integer()
    promotion_count = fields.Integer()

    def generate_promotion(self):
        self.gp_button_count += 1
        record = self.env['college.mark.sheet'].search(
            [('exam', '=', self.exam_id.name),
             ('class_name', '=', self.class_id.name)])
        for rec in record:
            if rec.pass_or_fail:
                qualified_student_ids = self.env['college.students'].search(
                    [('id', '=', rec.student_id.id)])
                self.qualified_student_ids = qualified_student_ids

    def Promote(self):
        # self.promotion_count += 1
        # self.state = 'completed'
        qualified_students = self.qualified_student_ids
        print(self.class_id.promotion_class.list_of_student_ids)
        self.class_id.promotion_class.list_of_student_ids = qualified_students
        print(self.class_id.promotion_class.list_of_student_ids)
        for rec in self.class_id.promotion_class.list_of_student_ids:
            rec.semester = self.class_id.promotion_class.semester_id.id
