odoo.define('braintree_payment_gateway.payment_form', require => {
    'use strict';

    const core = require('web.core');
    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');
    const rpc = require('web.rpc');

    const braintreeMixin = {
        _processDirectPayment: function(provider, acquirerId, processingValues) {
            if (provider !== 'braintree') {
                return this._super(...arguments);
            }
            this.dropinInstance.requestPaymentMethod(function(requestPaymentMethodErr, payload) {
                console.log("DDDDDDDDdd",processingValues)
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
        _prepareInlineForm:function (code, paymentOptionId, flow){
            if (code !== 'braintree'){
                return this._super(arguments)
            }
            else if (flow === 'token') {
                return Promise.resolve();
            }
            var self = this
            this._rpc({
                route: '/payment/braintree/get_token',
                params: {
                    'acquirer_id':paymentOptionId
                }
            }).then(token =>{
                self.token = token
                braintree.dropin.create({
                    authorization: token,
                    container: '#dropin-container'
                }).then(function(dropinInstance){
                    self.dropinInstance = dropinInstance
                })
            });
            this._setPaymentFlow('direct');
            return Promise.resolve()
        }
    };
    checkoutForm.include(braintreeMixin);
    manageForm.include(braintreeMixin);

});