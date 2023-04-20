from odoo import models, fields, api


class Semester(models.Model):
    _name = 'college.semester'
    _description = 'Semester'

    name = fields.Char(readonly=True, compute="_name_compute", store=True,
                       default=" ")
    number_of_semester = fields.Integer(string="Number Of Semester",
                                        required=True)
    course = fields.Many2one('college.course', string="Course")
    subject_id = fields.One2many('syllabus', 'semester', string="Subject")

    @api.depends('course.name', 'number_of_semester')
    def _name_compute(self):
        for rec in self:
            rec.name = str(rec.number_of_semester) + " Semester " + str(
                rec.course.name)

    # def get_syllabus(self):
    #     return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Syllabus',
    #             'view_mode': 'tree,form',
    #             'res_model': 'syllabus',
    #             'domain': [('semester.name', '=', self.name)]
    #     }
