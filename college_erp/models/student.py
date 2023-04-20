from odoo import models, fields, api


class CollegeStudents(models.Model):
    _name = 'college.students'
    _description = 'College Students'
    _rec_name = 'first_name'

    admission_no = fields.Char(string="Admission No")
    admission_date = fields.Date(string="Admission Date")
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    father = fields.Char(string="Father")
    mother = fields.Char(string="Mother")
    communication_address = fields.Text(string="Communication Address", )
    permanent_address = fields.Text(string="Permanent Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    semester = fields.Many2one('college.semester', string="Semester")
    course = fields.Many2one('college.course', string="Course")
    academic_year = fields.Char(string="Academic Year")
    class_id = fields.Many2one('college.class')
    promotion_class = fields.Many2one('college.class.promotion')
    mark_sheet_id = fields.Char()


class CollegeStudentSubject(models.Model):
    _name = 'college.student.subject'
    _description = 'College Student Subject'

    name = fields.Many2one('syllabus', string="Subject",
                           domain="[('semester', '=', semester),('course', '=', course)]",
                           required=True)
    course = fields.Many2one('college.course', string="Course", required=True)
    semester = fields.Many2one('college.semester', string="Semester",
                               required=True,
                               domain="[('course', '=', course)]")
    exam_id = fields.Many2one('college.mark.sheet')
    mark = fields.Integer(string='Mark', required=True)
    pass_mark = fields.Integer(string="Pass Mark", related='name.pass_mark')
    max_mark = fields.Integer(string="Maximum Mark", related='name.max_mark')
    pass_or_fail = fields.Boolean(string='Pass/Fail',
                                  compute='_compute_pass_or_fail', store=True)

    @api.depends('pass_mark', 'mark')
    def _compute_pass_or_fail(self):
        for rec in self:
            if rec.mark >= rec.pass_mark:
                rec.pass_or_fail = True
            else:
                rec.pass_or_fail = False
