from odoo import models, _
from odoo.exceptions import ValidationError


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'braintree' or len(tx) == 1:
            return tx
        reference = notification_data.get('reference')
        tx = self.search([('reference', '=', reference),
                          ('provider_code', '=', 'braintree')])
        if not tx:
            raise ValidationError(
                "Braintree: " + _(
                    "No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'braintree':
            return
        self._set_done()
