from odoo import models, fields
import xlsxwriter
import json
import io
from odoo.tools import date_utils


class MarkSheetReport(models.TransientModel):
    _name = 'mark.sheet.report'

    report_type = fields.Selection([
        ('student_wise', 'Student Wise'),
        ('class_wise', 'Class Wise')
    ], default='student_wise', required=True)
    student_id = fields.Many2one('college.students', string='Student',
                                 )
    class_id = fields.Many2one('college.class', string='Class')
    semester = fields.Many2one('college.semester', string='Semester',
                               required=True)
    exam_type = fields.Selection(
        [('internal', 'Internal'), ('semester', 'Semester'),
         ('unit_test', 'Unit Test')], string='Exam Type', required=True)

    # def _prepare_data_student(self):
    #     return data

    # def _prepare_date_class(self):

    def action_print(self):
        if self.report_type == 'student_wise':
            self.env.cr.execute(
                """select college_student_subject.mark,college_exam.exam_type,
                college_students.id,college_students.first_name,
                college_semester.number_of_semester, 
                college_course.name as course_name,
                college_students.academic_year,
                college_mark_sheet.pass_or_fail as exam_pass_or_fail,
                college_student_subject.pass_or_fail as subject_pass_or_fail
                ,syllabus.name,syllabus.pass_mark from college_student_subject 
                inner join 
                syllabus on syllabus.id = college_student_subject.name
                inner join 
                college_semester on college_semester.id = 
                college_student_subject.semester
                inner join 
                college_course ON college_course.id = college_semester.course
                inner join 
                college_mark_sheet on college_mark_sheet.id = 
                college_student_subject.exam_id
                inner join 
                college_students on college_students.id = 
                college_mark_sheet.student_id
                inner join 
                college_exam on college_exam.id = college_mark_sheet.exam
                where college_students.id=%s and college_mark_sheet.semester=%s 
                and college_exam.exam_type='%s';""" % (
                    self.student_id.id, self.semester.number_of_semester,
                    self.exam_type))
            record = self.env.cr.dictfetchall()
            print(record)
            result = ''
            for i in record:
                if i['exam_pass_or_fail']:
                    result = 'Pass'
                else:
                    result = 'Fail'
                    break
            data = {
                'form': self.read(),
                'course': self.semester.course.name,
                'academic_year': self.student_id.academic_year,
                'result': result,
                'data': record
            }
            print(data)
            return self.env.ref(
                'college_erp.action_mark_sheet_student').report_action(
                self,
                data=data)
        else:
            self.env.cr.execute("""SELECT college_students.id as student_id,
            array_agg(college_student_subject.mark) mark,
            college_students.first_name,
            ARRAY_agg(college_mark_sheet.pass_or_fail) pass_or_fail,
            array_agg(syllabus.name) subject,
            array_agg(syllabus.pass_mark) pass_mark,
            array_agg(syllabus.max_mark) max_mark,
            array_agg(college_class.id)class_id,array_agg(college_semester.id) 
            semester, array_agg(college_exam.exam_type) exam_type
            from college_student_subject 
            inner join syllabus on syllabus.id=college_student_subject.name
            inner join college_mark_sheet ON college_mark_sheet.id = 
            college_student_subject.exam_id
            inner join college_students on college_students.id = 
            college_mark_sheet.student_id
            inner join college_class ON college_class.id = 
            college_students.class_id
            inner join college_semester ON college_semester.id = 
            college_student_subject.semester
            inner join college_exam on college_exam.id = 
            college_mark_sheet.exam
            where college_class.id=%s and college_semester.id=%s and
            college_exam.exam_type='%s'
            group by 1;""" % (
                self.class_id.id, self.semester.number_of_semester,
                self.exam_type))
            record = self.env.cr.dictfetchall()
            count = 0
            count_of_sub = 0
            sub = []
            for i in record:
                if len(i['subject']) > count_of_sub:
                    count_of_sub = len(i['subject']) + 1
                    for c in range(1, count_of_sub):
                        sub.append(c)
                for j in i['pass_or_fail']:
                    c = 0
                    if not j:
                        c += 1
                        count += 1
                        break
            print(sub)
            data = {
                'form': self.read(),
                'fail_count': count,
                'count_of_sub': sub,
                'course': self.class_id.course_id.name,
                'academic_year': self.class_id.academic_year,
                'data': record
            }
            print(data)
            return self.env.ref(
                'college_erp.action_mark_sheet_class').report_action(self,
                                                                     data=data)

    def action_print_xlsx(self):
        if self.report_type == 'student_wise':
            self.env.cr.execute(
                """select college_student_subject.mark,college_exam.exam_type,
                college_students.id,college_students.first_name,
                college_semester.number_of_semester, 
                college_course.name as course_name,
                college_students.academic_year,
                college_mark_sheet.pass_or_fail as exam_pass_or_fail,
                college_student_subject.pass_or_fail as subject_pass_or_fail
                ,syllabus.name,syllabus.pass_mark from college_student_subject 
                inner join 
                syllabus on syllabus.id = college_student_subject.name
                inner join 
                college_semester on college_semester.id = 
                college_student_subject.semester
                inner join 
                college_course ON college_course.id = college_semester.course
                inner join 
                college_mark_sheet on college_mark_sheet.id = 
                college_student_subject.exam_id
                inner join 
                college_students on college_students.id = 
                college_mark_sheet.student_id
                inner join 
                college_exam on college_exam.id = college_mark_sheet.exam
                where college_students.id=%s and college_mark_sheet.semester=%s 
                and college_exam.exam_type='%s';""" % (
                    self.student_id.id, self.semester.number_of_semester,
                    self.exam_type))
            record = self.env.cr.dictfetchall()
            result = ''
            for i in record:
                if i['exam_pass_or_fail']:
                    result = 'Pass'
                else:
                    result = 'Fail'
                    break
            data = {
                'form': self.read(),
                'course': self.semester.course.name,
                'academic_year': self.student_id.academic_year,
                'result': result,
                'data': record
            }
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'mark.sheet.report',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'sss'},
                'report_type': 'xlsx',
            }
        else:
            self.env.cr.execute("""SELECT college_students.id as student_id,
             array_agg(college_student_subject.mark) mark,
             college_students.first_name,
             ARRAY_agg(college_mark_sheet.pass_or_fail) pass_or_fail,
             array_agg(syllabus.name) subject,
             array_agg(syllabus.pass_mark) pass_mark,
             array_agg(syllabus.max_mark) max_mark,
             array_agg(college_class.id)class_id,array_agg(college_semester.id) 
             semester, array_agg(college_exam.exam_type) exam_type
             from college_student_subject 
             inner join syllabus on syllabus.id=college_student_subject.name
             inner join college_mark_sheet ON college_mark_sheet.id = 
             college_student_subject.exam_id
             inner join college_students on college_students.id = 
             college_mark_sheet.student_id
             inner join college_class ON college_class.id = 
             college_students.class_id
             inner join college_semester ON college_semester.id = 
             college_student_subject.semester
             inner join college_exam on college_exam.id = 
             college_mark_sheet.exam
             where college_class.id=%s and college_semester.id=%s and
             college_exam.exam_type='%s'
             group by 1;""" % (
                self.class_id.id, self.semester.number_of_semester,
                self.exam_type))
            record = self.env.cr.dictfetchall()
            count = 0
            count_of_sub = 0
            sub = []
            for i in record:
                if len(i['subject']) > count_of_sub:
                    count_of_sub = len(i['subject']) + 1
                    for c in range(1, count_of_sub):
                        sub.append(c)
                for j in i['pass_or_fail']:
                    c = 0
                    if not j:
                        c += 1
                        count += 1
                        break
            print(sub)
            data = {
                'form': self.read(),
                'fail_count': count,
                'count_of_sub': sub,
                'course': self.class_id.course_id.name,
                'academic_year': self.class_id.academic_year,
                'data': record
            }
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'mark.sheet.report',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'sss'},
                'report_type': 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        for i in data['form']:
            if i['report_type'] == 'student_wise':
                student_name = data['form'][0]['student_id'][1]
                course = data['course']
                academic_year = data['academic_year']
                output = io.BytesIO()
                workbook = xlsxwriter.Workbook(output, {'in_memory': True})
                sheet = workbook.add_worksheet()
                head = workbook.add_format(
                    {'align': 'center', 'bold': True, 'font_size': '20px'})
                head2 = workbook.add_format(
                    {'align': 'center', 'bold': True, 'font_size': '13px'})
                head3 = workbook.add_format(
                    {'align': 'left', 'bold': True, 'font_size': '11px'})
                txt = workbook.add_format({'font_size': '10px'})
                sheet.merge_range('G5:H6', student_name + ": Mark List", head)
                sheet.merge_range('G7:H7', course + "-" + academic_year, head2)
                sheet.set_column(5, 9, 25)
                sheet.write('F13', 'Subject', head2)
                sheet.write('G13', 'Mark', head2)
                sheet.write('H13', 'Pass Mark', head2)
                sheet.write('I13', 'Pass/Fail', head2)
                sheet.write('F8', 'Exam: ' + data['form'][0]['exam_type'],
                            head3)
                for exam_pass in data['data']:
                    if exam_pass['exam_pass_or_fail']:
                        sheet.write('F9', 'Result: Pass', head3)
                        break
                    else:
                        sheet.write('F9', 'Result: Fail', head3)
                        break
                subject = []
                mark = []
                pass_mark = []
                pass_or_fail = []
                for j in data['data']:
                    subject.append(j['name'])
                    mark.append(j['mark'])
                    pass_mark.append(j['pass_mark'])
                    if j['subject_pass_or_fail']:
                        pass_or_fail.append('Pass')
                    else:
                        pass_or_fail.append('Fail')
                sheet.write_column('F14', subject, txt)
                sheet.write_column('G14', mark, txt)
                sheet.write_column('H14', pass_mark, txt)
                sheet.write_column('I14', pass_or_fail, txt)
                workbook.close()
                output.seek(0)
                response.stream.write(output.read())
                output.close()
            else:
                class_name = data['form'][0]['class_id'][1]
                course = data['course']
                academic_year = data['academic_year']
                output = io.BytesIO()
                workbook = xlsxwriter.Workbook(output, {'in_memory': True})
                sheet = workbook.add_worksheet()
                head = workbook.add_format(
                    {'align': 'center', 'bold': True, 'font_size': '20px'})
                head2 = workbook.add_format(
                    {'align': 'center', 'bold': True, 'font_size': '13px'})
                head3 = workbook.add_format(
                    {'align': 'left', 'bold': True, 'font_size': '11px'})
                txt = workbook.add_format({'font_size': '10px'})
                sheet.merge_range('F5:L6', class_name + ": Mark List", head)
                sheet.merge_range('G7:J7', course + "-" + academic_year, head2)
                sheet.set_column(5, 11, 18)
                sheet.write('F15', 'Student Name', head2)
                title = []
                for s in data['count_of_sub']:
                    title.append('paper' + str(s))
                title.append('Obtained Mark')
                title.append('Total Mark')
                title.append('Pass/Failed')
                sheet.write_row('G15', title, head2)
                sheet.write('F9', 'Exam: ' + data['form'][0]['exam_type'],
                            head3)
                co = 0
                for c in data['data']:
                    co += 1
                sheet.write('F10', 'Total: ' + str(co), head3)
                sheet.write('F12', 'Fail: ' + str(data['fail_count']), head3)
                sheet.write('F11', 'Pass: ' + str(co - data['fail_count']),
                            head3)
                row = 16
                for d in data['data']:
                    title_value = [d['first_name']]
                    for m in d['mark']:
                        title_value.append(m)
                    title_value.append(sum(d['mark']))
                    title_value.append(sum(d['pass_mark']))
                    for p in d['pass_or_fail']:
                        if not p:
                            title_value.append('Fail')
                            break
                        else:
                            title_value.append('Pass')
                            break
                    sheet.write_row('F' + str(row), title_value, txt)
                    row += 1
                workbook.close()
                output.seek(0)
                response.stream.write(output.read())
                output.close()
