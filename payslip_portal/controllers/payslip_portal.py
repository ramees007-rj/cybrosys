from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalPaySlip(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'payslip_count' in counters:
            values['payslip_count'] = request.env[
                'hr.payslip'].sudo().search_count(
                [('employee_id.user_id.id', '=', request.uid)])
        return values

    @http.route(['/my/payslip'], auth="user", website=True)
    def portal_payslip(self):
        values = {
            'payslips': request.env['hr.payslip'].sudo().search(
                [('employee_id.user_id.id', '=', request.uid)]),
            'page_name': 'my_payslips'
        }
        return request.render('payslip_portal.portal_payslip', values)

    @http.route(['/my/payslip/<int:p_id>'], type='http', auth="user",
                website=True)
    def portal_payslip_download(self, p_id):
        payslip = request.env['hr.payslip'].sudo().browse(int(p_id))
        print(payslip)
        vals = {
            'docs': payslip
        }
        pdf = request.env.ref(
            'payslip_portal.payslip_de_report').with_context(
            vals)._render_qweb_pdf([payslip.id])[0]
        print(pdf)
        pdfhttpheaders = [('Content-Type', 'application/pdf'),
                          ('Content-Length', len(pdf)), ]
        return request.make_response(pdf, headers=pdfhttpheaders)
