odoo.define('pos_product_brand.brand_name', function(require){
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('product.product','brand_name')
    var _super_order_line= models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options){
            var line= _super_order_line.initialize.apply(this,arguments)
            this.brand_name=this.product.brand_name;
        },
        export_for_printing:function(){
            var line= _super_order_line.export_for_printing.apply(this,arguments);
            line.brand_name=this.brand_name;
            return line;
        },
    })
})
