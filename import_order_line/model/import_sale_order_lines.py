from odoo import models, fields
import xlrd
import base64


class ImportOrderLine(models.Model):
    _inherit = 'sale.order'

    def action_import_order_lines(self):
        context = {'default_sale_order_ref': self.name}
        return {
            'name': 'xls File',
            'res_model': 'xls.file',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': context,
            'target': 'new',
        }


class XlsFile(models.TransientModel):
    _name = 'xls.file'

    xls_file = fields.Binary(string='Xls File', store=True)
    sale_order_ref = fields.Char()

    def action_import(self):
        record = self.env['sale.order'].search(
            [('name', 'like', self.sale_order_ref)])
        print(record)
        wb = xlrd.open_workbook(
            file_contents=base64.decodebytes(self.xls_file))
        row_vals = []
        for sheet in wb.sheets():
            for row in range(1, sheet.nrows):
                row_vals.append(sheet.row_values(row))
        for i in row_vals:
            product_id = self.env['product.product'].search(
                [('product_tmpl_id.name', '=', i[0])], limit=1)
            uom_id = self.env['uom.uom'].search([('name', '=', i[2])], limit=1)
            if len(product_id) is 0:
                print("if")
                product_id = self.env['product.template'].create({
                    'name': i[0]
                })
                product = self.env['product.product'].search(
                    [('product_tmpl_id', '=', product_id.id)])
                record.order_line.create({
                    'order_id': record.id,
                    'product_id': product.id,
                    'name': i[3],
                    'product_uom_qty': i[1],
                    'product_uom': uom_id.id,
                    'price_unit': i[4],
                    'customer_lead': 2
                })
            else:
                product = self.env['product.product'].search(
                    [('product_tmpl_id.name', '=', i[0])], limit=1)
                print(product_id, "4")
                print(uom_id, "4")
                record.order_line.create({
                    'order_id': record.id,
                    'product_id': product.id,
                    'name': i[3],
                    'product_uom_qty': i[1],
                    'product_uom': uom_id.id,
                    'price_unit': i[4],
                    'customer_lead': 2
                })
        # for col in range(sheet.ncols):
        #     print(sheet.cell(row, col).value)
        # # print(val)
