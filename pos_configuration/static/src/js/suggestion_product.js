/* global waitForWebfonts */
odoo.define('point_of_sale.modelsSuggestionProduct', function(require){
    "use strict";
    var { Product } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const ajax = require('web.ajax');
    var res;
    const GetSuggestionProduct = (Product) => class GetSuggestionProduct extends Product {
        get_suggestion_product_ids() {
            if (this.suggestion_product_ids.length != 0){
                ajax.jsonRpc('/suggestion_product', 'call', {'abcd':this.suggestion_product_ids})
                .then(function (result) {
                    res = result;
                    console.log(typeof result);
                });
                return res
        }
    }}
    Registries.Model.extend(Product, GetSuggestionProduct);
    });