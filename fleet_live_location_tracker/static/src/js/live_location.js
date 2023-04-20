odoo.define('fleet_location.live_location', function (require){
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var session = require('web.session');
    var count = 0
    var map;
    var marker, circle;
    var FleetLiveLocation = AbstractAction.extend({
        template: 'FleetLocation',
        context: false,
        init: function(parent, context) {
           this.context = context;
           this._super(parent, context);
        },
     events:{
        'click #fleet_map': 'load_live_location',
     },
     start: function() {
        var self = this;
        this.set("title", 'Dashboard');
        return this._super().then(function() {
            if (self.$el.find('#fleet_map').length > 0) {
//                self.load_live_location();
            } else {
                console.log('Map element not found in template');
            }
        });
    },
        load_live_location: function(){
            var self = this
            console.log(self.context.params)
            if (self.context.params.active_id){
                console.log(self.context.params.active_id)
            }else{
                console.log("hhhh")
            }
//            map = L.map('fleet_map').setView([14.0860746, 100.608406], 6);
//            //osm layer
//            var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//            });
//            osm.addTo(map);

//            if(!navigator.geolocation) {
//                console.log("Your browser doesn't support geolocation feature!")
//            } else {
//                setInterval(() => {
//                    navigator.geolocation.getCurrentPosition(self.getPosition)
//                }, 5000);
//            }
//
//            var marker, circle;
//            var count = 0 ;
//
//            rpc.query({
//                route: `/location/${self.context.params.active_id}`,
//                params: {}
//            }).then(function(res){
//
//            })
        },
        getPosition: function(position){
            var lat = position.coords.latitude
            var long = position.coords.longitude
            var accuracy = position.coords.accuracy

            if(marker) {
                map.removeLayer(marker)
            }

            if(circle) {
                map.removeLayer(circle)
            }

//            marker = L.marker([lat, long])
//            circle = L.circle([lat, long], {radius: accuracy})

//            var featureGroup = L.featureGroup([marker, circle]).addTo(map)

//            map.fitBounds(featureGroup.getBounds())

            console.log("Your coordinate is: Lat: "+ lat +" Long: "+ long+ " Accuracy: "+ accuracy)
        }
    })
    core.action_registry.add('fleet_live_location', FleetLiveLocation);
    return FleetLiveLocation;
})