from odoo import http
from odoo.http import request


class Sales(http.Controller):
    @http.route(['/total_product_sold'], type="json", auth="public")
    def sold_total(self):
        track = request.env['website.track'].sudo().search(
            [('visitor_id', '=', request.env['website.visitor'].sudo().search(
                [('partner_id', '=', request.env['res.users'].browse(
                    request.uid).partner_id.id)]).id)])
        print(track.product_id)
        count = 1
        slide_active = []
        slide_1 = []
        slide_2 = []
        for i in track.product_id:
            if count <= 3:
                slide_active.append(i)
                count += 1
            elif 3 < count < 7:
                slide_1.append(i)
                count += 1
            else:
                slide_2.append(i)
                count += 1
                if count == 10:
                    break
        values = {
            'slide_active': slide_active,
            'slide_1': slide_1,
            'slide_2': slide_2,
        }
        print(values)
        response = http.Response(
            template='recent_product_snippet.basic_snippet',
            qcontext=values)
        return response.render()
