from odoo import models, fields, api


class Admission(models.Model):
    _name = 'admission'
    _description = 'Admission'
    _rec_name = 'application_no'

    application_no = fields.Char(string='Application No',
                                 readonly=True, default='New')
    admission_no = fields.Char(readonly=True, default='New')
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    father = fields.Char(string="Father")
    mother = fields.Char(string="Mother")
    communication_address = fields.Text(string="Communication Address")
    check = fields.Boolean("Same as Communication Address")
    permanent_address = fields.Text(string="Permanent Address",
                                    compute='_compute_permanent_address')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    course_id = fields.Many2one('college.course', string="Course")
    date_of_application = fields.Date(string="Date Of Application",
                                      default=fields.Date.today())
    academic_year = fields.Char(String='Academic Year')
    previous_educational_qualification = fields.Selection(
        [('higher_secondary', 'Higher Secondary'), ('ug', 'UG'), ('pg', 'PG')],
        string="Previous Educational Qualification")
    educational_institute = fields.Char(string="Educational Institute")
    certificate_check = fields.Boolean(string="Add Attachment", default=False)
    transfer_certificate = fields.Binary(string="Document")
    check_item = fields.Boolean(string="Same as Communication Address")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('application', 'Application'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
    ], string='Status', required=True, readonly=True, copy=False,
        default='draft')
    semester_id = fields.Many2one('college.semester', string="Semester")

    # @api.onchange("check_item")
    # def _onchange_check_item(self):
    #     if self.check_item:
    #         self.permanent_address = self.communication_address
    #     else:
    #         self.permanent_address = None
    @api.depends('check_item')
    def _compute_permanent_address(self):
        for rec in self:
            if rec.check_item:
                rec.permanent_address = rec.communication_address
            else:
                rec.permanent_address = None

    def button_set_draft(self):
        for rec in self:
            rec.state = 'draft'

    def button_confirm(self):
        self['application_no'] = self.env['ir.sequence'].next_by_code(
            'application.no')
        print(self.application_no)
        self.state = 'application'

    def button_done(self):
        self['admission_no'] = self.env['ir.sequence'].next_by_code(
            'admission.no')
        self.env['college.students'].create({'admission_no': self.admission_no,
                                             'admission_date': fields.Date.today(),
                                             'first_name': self.first_name,
                                             'last_name': self.last_name,
                                             'father': self.father,
                                             'mother': self.mother,
                                             'communication_address': self.communication_address,
                                             'permanent_address': self.permanent_address,
                                             'phone': self.phone,
                                             'course':
                                                 self.course_id.id,
                                             'semester':
                                                 self.semester_id.id,
                                             'academic_year': self.academic_year, })
        mail_template = self.env.ref("college_erp.email_template_confirm")
        mail_template.send_mail(self._origin.id, force_send=True)
        self.state = 'done'

    def button_reject(self):
        mail_template = self.env.ref("college_erp.email_template_cancel")
        mail_template.send_mail(self._origin.id, force_send=True)
        self.state = 'rejected'

    def button_approved(self):
        self.state = 'approved'

# @api.depends("first_name")
# def _computed(self):
#     for rec in self:
#         rec.first_name = rec.first_name.first_name
