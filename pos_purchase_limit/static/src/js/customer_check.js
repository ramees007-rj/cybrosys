odoo.define('pos_purchase_limit.onclick_payment', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    models.load_fields('res.partner',['purchase_limit','active_purchase_limit'])
    const PosCustomerAlert = (ProductScreen) =>
        class extends ProductScreen {
            async _onClickPay() {
            if(this.currentOrder.get_client()){
                console.log(this.currentOrder.get_client().purchase_limit)
                if(this.currentOrder.get_client().active_purchase_limit){
                    if(this.currentOrder.get_client().purchase_limit<this.currentOrder.get_total_with_tax()){
                        console.log(this.showPopup('ErrorPopup',{
                        body: this.env._t('You are already reached purchase limit'),
                        }));
                        }
                    else{
                        await super._onClickPay();
                    }
                }
                else{
                    await super._onClickPay();
                }
            }
            else{
                console.log(this.showPopup('ErrorPopup',{
                    body: this.env._t('Select a Customer'),
                }));
            }
            }
        };
    Registries.Component.extend(ProductScreen, PosCustomerAlert);

    return ProductScreen;
});
