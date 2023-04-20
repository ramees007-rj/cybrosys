odoo.define('braintree_payment_gateway.payment_form', require => {
    'use strict';

    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');
    var rpc = require('web.rpc');

    const paymentBraintreeMixin = {

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Simulate a feedback from a payment provider and redirect the customer to the status page.
         *
         * @override method from payment.payment_form_mixin
         * @private
         * @param {string} provider - The provider of the acquirer
         * @param {number} acquirerId - The id of the acquirer handling the transaction
         * @param {object} processingValues - The processing values of the transaction
         * @return {Promise}
         */
        _processDirectPayment: function(provider, acquirerId, processingValues) {
            if (provider !== 'braintree') {
                return this._super(...arguments);
            }
            console.log(this.dropinInstance)
            this.dropinInstance.requestPaymentMethod(function(requestPaymentMethodErr, payload) {
                return rpc.query({
                    route: '/payment/braintree/process_payment',
                    params: {
                        'reference': processingValues.reference,
                        'payload': payload,
                        'data': processingValues
                    },
                }).then(() => {
                    window.location = '/payment/status';
                });
            });
        },

        /**
         * Prepare the inline form of Test for direct payment.
         *
         * @override method from payment.payment_form_mixin
         * @private
         * @param {string} provider - The provider of the selected payment option's acquirer
         * @param {integer} paymentOptionId - The id of the selected payment option
         * @param {string} flow - The online payment flow of the selected payment option
         * @return {Promise}
         */
        _prepareInlineForm: function(provider, paymentOptionId, flow) {
            if (provider !== 'braintree') {
                return this._super(...arguments);
            } else if (flow === 'token') {
                return Promise.resolve();
            }
            var self = this
            this._rpc({
                route: '/payment/braintree/get_token',
                params: {
                    'acquirer_id': paymentOptionId,
                },
            }).then(token => {
                self.token = token
                braintree.dropin.create({
                    authorization: token,
                    container: '#dropin-container'
                }).then(function(dropinInstance) {
                    self.dropinInstance = dropinInstance
                })
            });
            this._setPaymentFlow('direct');
            return Promise.resolve()
        },
    };
    checkoutForm.include(paymentBraintreeMixin);
    manageForm.include(paymentBraintreeMixin);
});