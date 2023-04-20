from odoo import models, fields, api


class DiscountLimit(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_limits = fields.Float(string="Discount Limit")

    def set_values(self):
        super(DiscountLimit, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('discount_approval.discount_limits',
                  int(self.discount_limits))
        print(set_param)

    @api.model
    def get_values(self):
        res = super(DiscountLimit, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['discount_limits'] = int(
            get_param('discount_approval.discount_limits'))
        return res


class DiscountLimitSaleOrder(models.Model):
    _inherit = 'sale.order'

    check = fields.Boolean(default=False)
    check_approval = fields.Boolean(default=False)
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('approval', 'Waiting for Approval'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3,
        default='draft')

    @api.onchange('order_line')
    def _onchange_order_line_discount(self):
        limit = self.env['res.config.settings'].search([])[
            -1].discount_limits
        for rec in self.order_line:
            if rec.discount > limit:
                self.check = True
                break
            else:
                self.check = False

    def button_request_approval(self):
        self.state = 'approval'

    def accept(self):
        self.action_confirm()

    def reject(self):
        self.action_cancel()
