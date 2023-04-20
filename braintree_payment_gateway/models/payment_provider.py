from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import braintree


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('braintree', "BrainTree")],
        ondelete={'braintree': 'set default'})
    merchant_id = fields.Char('Merchant ID')
    public_key = fields.Char('Public Key')
    private_key = fields.Char('Private Key')

    def write(self, vals):
        res = super(PaymentProvider, self).write(vals)
        if self.code != 'braintree':
            return res
        if self.state == 'enabled':
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox

        if self.merchant_id and self.private_key and self.public_key:
            try:
                gateway = braintree.BraintreeGateway(
                    braintree.Configuration(
                        environment=environment,
                        merchant_id='wvn354htkf6wbhcv',
                        public_key='n992z4xpcvc4pxtk',
                        private_key='9e5a850e05996214799373f942e912e2'
                    ))
                token = gateway.client_token.generate()
            except:
                raise ValidationError(_('Invalid Credentials!'))

        return res


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['braintree'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res
