from odoo import http
from odoo.http import request


class Sales(http.Controller):
    @http.route(['/product'], type="json", auth="public")
    def product(self):
        values = {
            'key': request.env['product.product'].search([], limit=1)
        }
        print("product:",request.env['product.product'].search_read([],limit=1))
        response = http.Response(
            template='snippet_16.basic_snippet',
            qcontext=values)
        return response.render()
