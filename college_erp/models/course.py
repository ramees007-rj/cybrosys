from odoo import models, fields, api


class CollegeCourse(models.Model):
    _name = "college.course"
    _description = "College Course"

    name = fields.Char(string="Name", required=True)
    category = fields.Selection(
        [('ug', 'Under Graduation'), ('pg', 'Post Graduation'),
         ('diploma', 'Diploma')], string="Category")
    duration = fields.Integer(string="Duration(year)", required=True)
    no_of_semester = fields.Integer(string="Number Of Semester")
    semester_ids = fields.One2many('college.semester', 'course',
                                  string='Semester')

    # @api.depends('semester_id')
    # def _compute_semester_id(self):
    #     for rec in self:
    #         rec.semester_id.course = rec.name

    # def get_semester(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Semester',
    #         'view_mode': 'tree,form',
    #         'res_model': 'college.semester',
    #         'domain': [('course.name', '=', self.name)]
    #     }
    # @api.depends('semester_id')
    # def _compute_semester_id(self):
    #     view_id = self.env.ref(
    #         'college.semester.configuration_semester_form').id
    #     print(view_id)
        # context = {'default_event': self.id}
        #
        # print(context)
        # return {
        #     'name': 'form_name',
        #     'view_type': 'form',
        #     'views': [(view_id, 'form')],
        #     'res_model': 'catering',
        #     'view_id': view_id,
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        #     'context': context,
        # }
