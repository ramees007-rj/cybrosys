from odoo import models, fields, api


class CollegeClass(models.Model):
    _name = 'college.class'
    _description = 'College Class'

    name = fields.Char(string='Name', raadonly=True, compute='_compute_name')
    semester_id = fields.Many2one('college.semester', string="Semester")
    course_id = fields.Many2one('college.course', string="Course")
    academic_year = fields.Selection(
        'year_selection',
        string="Academic Year",
        default="2022",
    )
    promotion_class = fields.Many2one('college.class',
                                      string='Promotion class')
    list_of_student_ids = fields.One2many('college.students', 'class_id',
                                          string="Student List")

    def year_selection(self):
        year = 2000
        year_list = []
        while year != 2030:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    def _compute_name(self):
        for record in self:
            record.name = str(record.semester_id.name) + str(
                "(" + str(record.academic_year) + ")")

    @api.onchange('semester_id', 'academic_year', 'course_id')
    def add_lines_ids(self):
        for rec in self:
            record_ids = self.env['college.students'].search(
                [('academic_year', '=', self.academic_year),
                 ('semester.id', '=', self.semester_id.id),
                 ('course.id', '=', self.course_id.id)])
            rec.list_of_student_ids = record_ids
