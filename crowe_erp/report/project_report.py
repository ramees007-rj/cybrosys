from odoo import fields, models
import json
from odoo.tools import date_utils
import io

project_ids = None
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ProjectReport(models.TransientModel):
    _name = 'project.crowe.report'

    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    customer_id = fields.Many2one('res.partner', string='Customer')
    user_id = fields.Many2one('res.users', string='Project Manager')
    project_ids = fields.Many2many('project.project', string='Projects')

    def action_print_report(self):
        global project_ids
        if self.from_date and self.to_date and self.project_ids and self.customer_id and self.user_id:
            print("g")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('create_date', '<', self.to_date),
                 ('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id),
                 ('user_id', '=', self.user_id.id)])
        elif self.from_date and self.to_date and self.customer_id and self.user_id:
            print(15)
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('create_date', '<', self.to_date),
                 ('sale_order_id.partner_id', '=', self.customer_id.id),
                 ('user_id', '=', self.user_id.id)])
        elif self.from_date and self.to_date and self.project_ids and self.customer_id:
            print("f")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('create_date', '<', self.to_date),
                 ('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id)])
        elif self.to_date and self.project_ids and self.customer_id and self.user_id:
            print(6)
            project_ids = self.env['project.project'].search(
                [('create_date', '<', self.from_date),
                 ('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id),
                 ('user_id', '=', self.user_id.id)])
        elif self.project_ids and self.customer_id and self.user_id:
            print(9)
            project_ids = self.env['project.project'].search(
                [('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id),
                 ('user_id', '=', self.user_id.id)])
        elif self.project_ids and self.customer_id and self.from_date:
            print(10)
            project_ids = self.env['project.project'].search(
                [('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id),
                 ('create_date', '>', self.from_date)])
        elif self.project_ids and self.user_id and self.from_date:
            print(11)
            project_ids = self.env['project.project'].search(
                [('id', 'in', self.project_ids.mapped('id')),
                 ('user_id', '=', self.user_id.id),
                 ('create_date', '>', self.from_date)])
        elif self.project_ids and self.customer_id and self.to_date:
            print(12)
            project_ids = self.env['project.project'].search(
                [('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id),
                 ('create_date', '<', self.from_date)])
        elif self.project_ids and self.user_id and self.to_date:
            print(13)
            project_ids = self.env['project.project'].search(
                [('id', 'in', self.project_ids.mapped('id')),
                 ('user_id', '=', self.user_id.id),
                 ('create_date', '<', self.from_date)])
        elif self.from_date and self.to_date and self.project_ids:
            print("e")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('create_date', '<', self.to_date),
                 ('id', 'in', self.project_ids.mapped('id'))])
        elif self.to_date and self.project_ids and self.customer_id:
            print(4)
            project_ids = self.env['project.project'].search(
                [('create_date', '<', self.from_date),
                 ('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id)])
        elif self.from_date and self.to_date:
            print("a")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('create_date', '<', self.to_date)])
        elif self.from_date and self.project_ids:
            print("b")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('id', 'in', self.project_ids.mapped('id'))])
        elif self.from_date and self.customer_id:
            print("c")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('sale_order_id.partner_id', '=', self.customer_id.id)])
        elif self.from_date and self.user_id:
            print("d")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date),
                 ('user_id', '=', self.user_id.id)])
        elif self.to_date and self.project_ids:
            print(1)
            project_ids = self.env['project.project'].search(
                [('create_date', '<', self.from_date),
                 ('id', 'in', self.project_ids.mapped('id'))])
        elif self.to_date and self.customer_id:
            print(2)
            project_ids = self.env['project.project'].search(
                [('create_date', '<', self.from_date),
                 ('sale_order_id.partner_id', '=', self.customer_id.id)])
        elif self.to_date and self.user_id:
            print(3)
            project_ids = self.env['project.project'].search(
                [('create_date', '<', self.from_date),
                 ('user_id', '=', self.user_id.id)])
        elif self.project_ids and self.customer_id:
            print(7)
            project_ids = self.env['project.project'].search(
                [('id', 'in', self.project_ids.mapped('id')),
                 ('sale_order_id.partner_id', '=', self.customer_id.id)])
        elif self.project_ids and self.user_id:
            print(8)
            project_ids = self.env['project.project'].search(
                [('id', 'in', self.project_ids.mapped('id')),
                 ('user_id', '=', self.user_id.id)])
        elif self.customer_id and self.user_id:
            print(14)
            project_ids = self.env['project.project'].search(
                [('sale_order_id.partner_id', '=', self.customer_id.id),
                 ('user_id', '=', self.user_id.id)])
        elif self.from_date:
            print("fff")
            project_ids = self.env['project.project'].search(
                [('create_date', '>', self.from_date)])
        elif self.to_date:
            print("gg")
            project_ids = self.env['project.project'].search(
                [('create_date', '<', self.to_date)])
        elif self.project_ids:
            print("lll")
            project_ids = self.env['project.project'].browse(
                self.project_ids.mapped('id'))
        elif self.customer_id:
            print(";;;;;;;")
            project_ids = self.env['project.project'].search(
                [('sale_order_id.partner_id', '=', self.customer_id.id)])
        elif self.user_id:
            print(";;;;;")
            project_ids = self.env['project.project'].search(
                [('user_id', '=', self.user_id.id)])
        project_list = []
        for rec in project_ids:
            cost_lines = []
            task_details = []
            for task in rec.task_ids:
                user_details = []
                for user in task.user_ids:
                    user_details.append({
                        'employee_name': user.name,
                        'hours_spend': sum(task.timesheet_ids.search(
                            [('task_id', '=', task.id), ('employee_id', '=',
                                                         self.env[
                                                             'hr.employee'].search(
                                                             [('user_id', '=',
                                                               user.id)]).id)]).mapped(
                            'unit_amount')),
                        'cost': self.env['hr.employee'].search(
                            [('user_id', '=', user.id)]).hourly_cost * sum(
                            task.timesheet_ids.search(
                                [('task_id', '=', task.id), (
                                    'employee_id', '=',
                                    self.env['hr.employee'].search(
                                        [('user_id', '=',
                                          user.id)]).id)]).mapped(
                                'unit_amount'))
                    })
                    cost_lines.append(self.env['hr.employee'].search(
                        [('user_id', '=', user.id)]).hourly_cost * sum(
                        task.timesheet_ids.search([('task_id', '=', task.id), (
                            'employee_id', '=', self.env['hr.employee'].search(
                                [('user_id', '=', user.id)]).id)]).mapped(
                            'unit_amount')))
                task_details.append({
                    'task_name': task.name,
                    'user_details': user_details,
                    'Total_hours': sum(task.timesheet_ids.search(
                        [('task_id', '=', task.id)]).mapped('unit_amount')),
                    'proposal_amount': task.sale_line_id.price_subtotal,
                    'wo_com_date': self.env['work.order'].search(
                        [('task_id', '=', task.id)],
                        limit=1).date_of_commencement
                })
            project_list.append({
                'project_name': rec.name,
                'budgeted_hours': rec.estimated_hours,
                'Proposal_Amount': rec.sale_order_id.amount_total,
                'task_details': task_details,
                'total_hrs_spend': sum(
                    self.env['account.analytic.line'].search(
                        [('project_id', '=', rec.id)]).mapped('unit_amount')),
                'total_cost': sum(cost_lines)
            })
        print(project_list)
        data = {
            'data': project_list,
            'sss': 'sss'
        }
        return {'type': 'ir.actions.report',
                'report_type': 'xlsx',
                'data': {'model': 'project.crowe.report',
                         'output_format': 'xlsx',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),

                         'report_name': 'Excel Report Name', }, }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '15px',
             'bg_color': '#355269'})
        txt = workbook.add_format(
            {'font_size': '10px', 'bold': True, 'bg_color': '#ff9898'})
        txt2 = workbook.add_format(
            {'font_size': '10px', 'bold': True, 'bg_color': '#afd095'})
        txt1 = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('A1:L3', 'PROJECT ANALYTIC REPORT', head)
        sheet.write_row('A4', ['Project', 'Task', 'User', 'Total Hours',
                               'Budgeted Hours', 'HR Rate (Cost)',
                               'Proposal Amount (Task Wise)',
                               'Amount Invoiced', 'Amount Due',
                               'Task Status', 'Task Commencement',
                               'Task Deadline'], txt)
        row = 4
        for pro in data['data']:
            sheet.set_row(row, cell_format=txt2)
            sheet.write(int(row), 0, pro['project_name'], txt2)
            sheet.write(int(row), 4, pro['budgeted_hours'], txt2)
            sheet.write(int(row), 3, pro['total_hrs_spend'], txt2)
            total_hr_rate = []
            sheet.write(int(row), 5, sum(total_hr_rate), txt2)
            sheet.write(int(row), 6, pro['Proposal_Amount'], txt2)
            sheet.write(int(row), 5, pro['total_cost'], txt2)
            row += 1
            for rec in pro['task_details']:
                sheet.write(int(row), 1, rec['task_name'], txt1)
                sheet.write(int(row), 6, rec['proposal_amount'], txt1)
                sheet.write(int(row), 10, rec['wo_com_date'], txt1)
                row += 1
                for user in rec['user_details']:
                    sheet.write(int(row), 2, user['employee_name'], txt1)
                    sheet.write(int(row), 3, user['hours_spend'], txt1)
                    sheet.write(int(row), 5, user['cost'], txt1)
                    total_hr_rate.append(user['cost'])
                    row += 1
        sheet.set_column(1, 100, 18)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()