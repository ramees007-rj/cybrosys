from odoo import fields, models, _


class ExcelReport(models.AbstractModel):
    _name = 'report.attendance_report.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Xlsx'

    def generate_xlsx_report(self, workbook, data, objs):
        sheet = workbook.add_worksheet('Report')
        head = workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_size': '15px',
        })
        txt = workbook.add_format({'font_size': '10px'})
        cell_format = workbook.add_format({
            'font_size': '10px',
        })
        sheet.merge_range('A2:F3', 'ATTENDANCE REPORT', head)
        sheet.write('B6', 'Date :', cell_format)
        sheet.merge_range('C6:D6', data['date'], txt)

        sheet.write('A10', 'SL/NO.', cell_format)
        sheet.write('B10', 'Employee Name', cell_format)
        sheet.write('C10', 'Department', cell_format)
        sheet.write('D10', 'Check In', cell_format)
        sheet.write('E10', 'Check Out', cell_format)
        sheet.write('F10', 'Worked Hours', cell_format)

        row = 11
        column = 0
        a = 1
        for i in data['query']:
            sheet.write(row, column, a)
            a = a + 1
            sheet.write(row, column + 1, i['name'])
            sheet.write(row, column + 2, i['department'])
            sheet.write(row, column + 3, i['check_in'])
            sheet.write(row, column + 4, i['check_out'])
            sheet.write(row, column + 5, i['round'])
            row += 1
