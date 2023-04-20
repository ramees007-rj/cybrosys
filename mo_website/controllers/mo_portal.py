from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalMoPage(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'mo_count' in counters:
            values['mo_count'] = request.env['mrp.production'].search_count(
                [('customer_id.id', '=',
                  request.env['res.users'].browse(request.uid).partner_id.id)])
        return values

    @http.route(['/my/mo'], auth="user", website=True)
    def portal_mo_page(self):
        values = {
            'mo_orders': request.env['mrp.production'].search(
                [(
                    'customer_id.id', '=',
                    request.env['res.users'].browse(
                        request.uid).partner_id.id)]),
            'page_name': 'mo_orders',

        }
        return request.render('mo_website.portal_my_mo', values)

    @http.route(['/my/mo/<int:mo_id>'], auth="user", website=True)
    def portal_mo_view(self, mo_id):
        values = {
            'mo_order_single': request.env['mrp.production'].browse([mo_id]),
            'page_name': 'mo_orders_view',
        }
        return request.render('mo_website.portal_my_mo_view', values)
