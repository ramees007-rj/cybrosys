from odoo import models, fields, api


class LocationPos(models.Model):
    _inherit = 'pos.config'

    location_id = fields.Many2one('stock.location', string='Source Location',
                                  domain="[('usage', '=', 'internal')]")


class ProductPosQuantity(models.Model):
    _inherit = 'product.product'

    pos_location_qty = fields.Integer()

    @api.model
    def get_location_quantity(self, pos_id):
        for j in self.env['product.product'].search([]):
            j.pos_location_qty = None
        for i in self.env['stock.quant'].search([('location_id', '=',
                                                  self.env[
                                                      'pos.config'].browse(
                                                      int(pos_id)).location_id.id)]):
            i.product_id.pos_location_qty = i.available_quantity

        # print(products.read())
        # print(products.product_id.pos_location_qty)

        # res = products._compute_quantities_dict(self._context.get('lot_id'),
        #                                         self._context.get('owner_id'),
        #                                         self._context.get(
        #                                             'package_id'),
        #                                         self._context.get('from_date'),
        #                                         self._context.get('to_date'))
        # variants_available = {
        #     p['id']: p for p in self.product_variant_ids.read(
        #         ['qty_available', 'virtual_available', 'incoming_qty',
        #          'outgoing_qty'])
        # }
        # print(variants_available)
        # for product in products:
        #     print("sss", res[product.id])

        # product = []
        # print(self.env['stock.quant'].search_count([]))
        # for rec in self.env['stock.quant'].search([]):
        #     if rec.location_id.id == self.env['pos.config'].browse(
        #             int(pos_id)).location_id.id:
        #         print("if")
        #         rec.product_id.pos_location_qty = rec.quantity
        #         product.append(rec.product_id.id)
        #     else:
        #         for i in product:
        #             if rec.product_id.id == i:
        #                 continue
        #             else:
        #                 rec.product_id.pos_location_qty = None
