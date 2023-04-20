import base64
from odoo import fields, models


class EmployeeAttendance(models.Model):
    _inherit = "hr.employee"

    def daily_attendance(self):
        date = fields.Date.today()
        today = fields.Date.today().day
        attendance = self.env['hr.attendance'].search([])
        today_list = []
        managers = []

        for rec in attendance:
            if rec.employee_id.parent_id.id not in managers:
                managers.append(rec.employee_id.parent_id.id)
            if rec.check_in and rec.check_out:
                if (rec.check_in.day and rec.check_out.day) == today:
                    today_list.append(
                        [rec.employee_id.name, rec.department_id.name, rec.check_in.time(), rec.check_out.time(),
                         round(rec.worked_hours), rec.employee_id.parent_id.id, rec.employee_id.parent_id.work_email])
                print(today_list)
        new_list = []
        for i in managers:
            for j in today_list:
                if i in j:
                    new_list.append(j)

            data = {
                'report_list': new_list,
                'date': date
            }
            report_template_id = self.env.ref(
                'attendance_report.action_employee_attendance_report_pdf')._render_qweb_pdf(self, data=data)
            data_record = base64.b64encode(report_template_id[0])
            ir_values = {
                'name': "Attendance Report",
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            }
            attachment1 = self.env['ir.attachment'].create(ir_values)

            sql = """select hre.name,hrp.name as manager,hrp.work_email,hrd.name as department,
                    cast(hra.check_in as time),cast(hra.check_out as time),round(hra.worked_hours)
                    from
                    hr_attendance hra
                    join
                    hr_employee hre
                    on hra.employee_id = hre.id
                    join
                    hr_department hrd
                    on
                    hre.department_id = hrd.id
                    join
                    hr_employee hrp
                    on hre.parent_id = hrp.id
                    where EXTRACT(
                    day FROM hra.check_in)='{check}' and EXTRACT(
                    day FROM hra.check_out)='{check}'""".format(check=today)

            self.env.cr.execute(sql)
            query = self.env.cr.dictfetchall()

            data = {
                'query': query,
                'date': date
            }
            report = self.env.ref('attendance_report.action_report_xlsx')
            generated_report = report._render_xlsx(self, data=data)
            data_record = base64.b64encode(generated_report[0])
            ir_values = {
                'name': 'Attendance Report',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/vnd.ms-excel',

            }
            attachment2 = self.env['ir.attachment'].sudo().create(ir_values)

            emails = ''
            for i in new_list:
                emails = emails + i[6] + ','
            mail_values = {
                "subject": "The Employee Attendance",
                "email_to": emails,
                "attachment_ids": [attachment1.id, attachment2.id]
            }

            mail = self.env["mail.mail"].sudo().create(mail_values)
            mail.send()
            new_list = []
