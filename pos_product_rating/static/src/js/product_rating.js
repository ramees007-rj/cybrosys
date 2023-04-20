odoo.define('pos_product_rating.product_rating',function(require){
    "use strict";

    var models = require('point_of_sale.models');
    models.load_fields('product.product','product_quality')
    var _super_order_line= models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
         export_for_printing:function(){
            var line= _super_order_line.export_for_printing.apply(this,arguments);
            line.product_quality=this.product.product_quality;
            return line;
        },
    })
})