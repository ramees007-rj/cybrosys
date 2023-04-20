odoo.define('POS_credit_limit.onclick_payment',function(require){
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const PosCreditLimit = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor(){
                super();
//                console.log("constructor called................")
            }
            async validateOrder(){
                const payment = this.paymentLines.filter(payment => payment.payment_method.split_transactions);
                if (payment.length == 1 && this.currentOrder.get_partner()){
                    if(this.currentOrder.get_partner().use_partner_credit_limit){
                        if(this.currentOrder.get_partner().credit + this.currentOrder.get_total_with_tax() > this.currentOrder.get_partner().credit_limit){
                            var credit_limit = this.currentOrder.get_partner().credit_limit;
                            var current_credit = this.currentOrder.get_partner().credit;
                            this.showPopup('ErrorPopup', {
                                title: this.env._t('Exceeding the credit limit'),
                                body: this.env._t("Sorry the credit allowed will reach it's limit(Credit Limit:" + credit_limit + ")." + "Your current credit is( " + current_credit + " ). Please pay using different payment method or contact manager")
                            })
                        }
                        else{
                            await super.validateOrder();
                        }
                    }
                    else{
                         this.showPopup('ErrorPopup', {
                            title: this.env._t('Credit not Allowed'),
                            body: this.env._t('This partner is not allowed for credit payment'),
                    })
                    }
                }
                else{
                   await super.validateOrder();
                }
            }
        }
    Registries.Component.extend(PaymentScreen, PosCreditLimit);
    return PaymentScreen;
});