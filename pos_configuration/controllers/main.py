from odoo import http
from odoo.http import request


class SuggestionProduct(http.Controller):

    @http.route('/suggestion_product', type='json', auth='public')
    def get_suggestion_product(self, abcd):
        product_list = []
        for rec in abcd:
            product = request.env['product.product'].browse(rec)
            product_list.append({
                'id': product.product_tmpl_id.id,
                'name': product.product_tmpl_id.name,
                'price': product.product_tmpl_id.list_price,

            })
        print(product_list)
        return product_list
