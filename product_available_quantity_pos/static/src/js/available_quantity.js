odoo.define('product_available_quantity_pos.ProductScreen', function (require) {
    'use strict';

    var rpc = require('web.rpc');
    const models=require('point_of_sale.models')
    models.load_fields('product.product','pos_location_qty')
    var _super_product= models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        after_load_server_data:function(){
            var line=_super_product.after_load_server_data.apply(this,arguments);
            console.log("line:",line)
            console.log(this.config_id)
            rpc.query({
                model: 'product.product',
                method: 'get_location_quantity',
                args: String(this.config_id)
            })
            return line;
        }
    })

});
