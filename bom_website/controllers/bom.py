from odoo import models, fields
from odoo.http import request


class Bom(models.Model):
    _inherit = 'sale.order.line'

    def get_product_material(self):
        print(self.env['website'].browse(request.website.id))
        website_id = self.env['website'].browse(request.website.id)
        mat = []
        for i in website_id.product:
            if self.product_id.product_tmpl_id.id == i.product_tmpl_id.id:
                material = self.env['mrp.bom.line'].search([('bom_id', '=',self.product_id.product_tmpl_id.bom_ids.id)])
                for rec in material:
                    mat.append({
                        'name': rec.product_id.name,
                        'qty': str(rec.product_qty)})
        print(mat)
        return mat


class WebsiteProductSelection(models.Model):
    _inherit = 'website'

    product = fields.Many2many('product.product', string="BOM Products")
