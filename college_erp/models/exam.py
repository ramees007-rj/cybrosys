from odoo import models, fields, api


class CollegeExam(models.Model):
    _name = 'college.exam'
    _description = 'College Exam'

    name = fields.Char(string="Name", readonly=True, compute='_compute_name',
                       default="New")
    class_id = fields.Many2one('college.class', string="Class",
                               required=True)
    semester = fields.Integer(
        related='class_id.semester_id.number_of_semester',
        string="Semester")
    exam_type = fields.Selection(
        [('internal', 'Internal'), ('semester', 'Semester'),
         ('unit_test', 'Unit Test')], required=True, string='Exam Type')
    course = fields.Char(related='class_id.course_id.name', string="Course")
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date",
                           required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'),
                              ('completed', 'Completed')], string="Status",
                             required=True, readonly=True, copy=False,
                             default='draft')
    paper_ids = fields.One2many('syllabus', 'exam_id', string="Papers")
    valuation_count = fields.Integer(compute='_compute_valuation_count')
    generate_mark_sheet_count = fields.Integer()

    @api.depends('class_id', 'exam_type')
    def _compute_name(self):
        for rec in self:
            rec.name = str(rec.exam_type) + " " + '(' + str(
                rec.semester) + " " + "Semester" + ')' + 'Exam'

    # @api.onchange('exam_type', 'semester', 'class_id')
    # def _onchange(self):
    #     for rec in self:
    #         for paper in rec.class_id.semester:
    #             print(paper)
    #             for pap in paper.subject_id:
    #                 lines = [(5, 0, 0)]
    #                 vals = {
    #                     'name': pap.name
    #                 }
    #                 # lines.append((0, 0, vals))
    #                 rec.write({"paper_id": [(0, 0, vals)]})

    @api.onchange('exam_type', 'semester', 'class_id')
    def add_lines_ids(self):
        if self.exam_type == 'semester':
            for rec in self:
                record_ids = self.env['syllabus'].search([
                    ('semester.id', '=', self.class_id.semester_id.id),
                    ('course.id', '=', self.class_id.course_id.id)])
                rec.paper_ids = record_ids
        else:
            for rec in self:
                rec.paper_ids = rec.paper_ids.create([])

    def button_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def button_complete(self):
        for rec in self:
            rec.state = 'completed'

    def button_action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def button_generate_mark(self):
        if self.generate_mark_sheet_count == 0:
            self.generate_mark_sheet_count = self.generate_mark_sheet_count + 1
            ids = []
            record = self.env['college.students'].search(
                [('class_id.id', '=', self.class_id.id)])
            for rec in record:
                self.env['college.mark.sheet'].create({
                    'student_id': rec.id,
                    'exam': self.id,
                    'class_name': self.class_id.id,
                })
                rec.mark_sheet_id = self.env['college.mark.sheet'].search([])[
                    -1].id
                ids.append(self.env['college.mark.sheet'].search([])[-1].id)
            return {
                'type': 'ir.actions.act_window',
                'name': 'College Mark Sheet',
                'view_mode': 'tree,form',
                'res_model': 'college.mark.sheet',
                'domain': [('id', '=', ids)]
            }
        else:
            record = self.env['college.students'].search(
                [('class_id.id', '=', self.class_id.id)])
            ids = []
            for rec in record:
                ids.append(rec.mark_sheet_id)
            return {
                'type': 'ir.actions.act_window',
                'name': 'College Mark Sheet',
                'view_mode': 'tree,form',
                'res_model': 'college.mark.sheet',
                'domain': [('id', '=', ids)]
            }

    # def get_mark_sheet(self):
    #     print("sssss")
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'College Mark Sheet',
    #         'view_mode': 'tree,form',
    #         'res_model': 'college.mark.sheet',
    #         # 'domain': [('mark_sheet_id', '=', ids)]
    #     }

    @api.depends('end_date')
    def action_date(self):
        record = self.env['college.exam'].search([])
        for rec in record:
            if rec.state == 'confirmed':
                if rec.end_date <= fields.Date.today():
                    rec.state = 'completed'
                else:
                    rec.state = 'confirmed'
            else:
                break

    def get_valuation(self):
        for rec in self:
            ids = []
            for record in rec.class_id.list_of_student_ids:
                ids.append(record.id)
            return {
                'type': 'ir.actions.act_window',
                'name': 'Student Details',
                'view_mode': 'tree,form',
                'res_model': 'college.students',
                'domain': [('id', 'in', ids)]
            }

    def _compute_valuation_count(self):
        for rec in self:
            ids = []
            for record in rec.class_id.list_of_student_ids:
                ids.append(record.id)
            rec.valuation_count = len(ids)
