odoo.define('custom_dashboard.dashboard_action', function (require){
  "use strict";
  var AbstractAction = require('web.AbstractAction');
  var core = require('web.core');
  var QWeb = core.qweb;
  var rpc = require('web.rpc');
  var ajax = require('web.ajax');
  var session = require('web.session');
  var CustomDashBoard = AbstractAction.extend({
     template: 'CRMdashboard',
     events: {'click #leads': '_onclicklead',
              'click #opportunity': '_opportunity',
              'change #filter':'_onchangefilter',
                },
     start: function() {
        var self = this;
        return this._super().then(function() {
            var start = new Date(new Date().getFullYear(), 0, 1)
            var end = new Date(new Date().getFullYear(), 11, 31)
            var list = { "key1" : start ,
                            "key2" : end ,
               };
           var com_id = session.company_id
            rpc.query({
                model: "crm.lead",
                method: "check_dashboard_values",
                args:[list,com_id]
            }).then(function(result){
                var ratio = (result['won_amount']/(result['won_amount']+result['lost_amount']))*100
                self.$el.find('#lead_count').text(result['lead_count']);
                self.$el.find('#opportunity_count').text(result['opportunity_count']);
                self.$el.find('#expected_revenue').text(result['currency'].concat(result['expected_revenue']));
                self.$el.find('#revenue').text(result['currency'].concat(result['revenue']));
                self.$el.find('#won_amount').text(result['currency'].concat(result['won_amount']));
                self.$el.find('#lost_amount').text(result['currency'].concat(result['lost_amount']));
                self.$el.find('#ratio').text(ratio.toFixed(2).concat('%'));
            })
            });
        },
     _onchangefilter: function(){
        var date = this._get_date()
        var com_id = session.company_id
        rpc.query({
            model: "crm.lead",
            method: "check_dashboard_values",
            args:[date,com_id]
        }).then(function(result){
            var ratio = (result['won_amount']/(result['won_amount']+result['lost_amount']))*100
            $('#lead_count').text(result['lead_count']);
            $('#opportunity_count').text(result['opportunity_count']);
            $('#expected_revenue').text(result['currency'].concat(result['expected_revenue']));
            $('#revenue').text(result['currency'].concat(result['revenue']));
            $('#won_amount').text(result['currency'].concat(result['won_amount']));
            $('#lost_amount').text(result['currency'].concat(result['lost_amount']));
            if (isNaN(ratio)){
                    $('#ratio').text('0'.concat('%'));
                }
            else{
                $('#ratio').text(ratio  .toFixed(2).concat('%'));
                }
        })
     },
    _get_date: function(){
         var filter_type = $('#filter :selected').val()
         if (filter_type == 'this_year'){
            var start = new Date(new Date().getFullYear(), 0, 1)
            var end = new Date(new Date().getFullYear(), 11, 31)
            var list = { "key1" : start ,
                            "key2" : end ,
               };
            return list

         }
         else if(filter_type == 'this_quarter'){
            var now = new Date();
            var quarter = Math.floor((now.getMonth() / 3));
            var firstDate = new Date(now.getFullYear(), quarter * 3, 1);
            var endDate = new Date(firstDate.getFullYear(), firstDate.getMonth() + 3, 0);
            var list = { "key1" : firstDate ,
                            "key2" : endDate ,
               };
            return list
         }
         else if(filter_type == 'this_month'){
             var date = new Date();
             var start = new Date(date.getFullYear(), date.getMonth(), 1);
             var end = new Date(date.getFullYear(), date.getMonth() + 1, 0);
             var list = { "key1" : start ,
                            "key2" : end ,
               };
             return list
         }
         else if(filter_type == 'this_week'){
            var curr = new Date;
            var first = curr.getDate() - curr.getDay();
            var last = first + 6;
            var start = new Date(curr.setDate(first)).toUTCString();
            var end = new Date(curr.setDate(last)).toUTCString();
            var list = { "key1" : start ,
                        "key2" : end ,
            };
            return list
         }
     },
     _onclicklead: function(){
            var self = this
            var filter_date = self._get_date()
            rpc.query({
                    model: "crm.lead",
                    method: "check_user_group",
                }).then(function(result){
                    var date = new Date();
                    if (result == true){
                        self.do_action({
                            name:'My Leads',
                            type: 'ir.actions.act_window',
                            res_model: 'crm.lead',
                            view_mode: 'tree,form,calendar',
                            views: [[false, 'list'],[false, 'form']],
                            domain: [['create_date', '>', filter_date['key1']], ['create_date', '<', filter_date['key2']]]
                        });
                    }
                    else{
                        self.do_action({
                            name:'My Leads',
                            type: 'ir.actions.act_window',
                            res_model: 'crm.lead',
                            view_mode: 'tree,form,calendar',
                            views: [[false, 'list'],[false, 'form']],
                            domain: [['user_id', '=', session.uid],['create_date', '>', filter_date['key1']], ['create_date', '<', filter_date['key2']]],
                        });
                    }
                })
          },
          _opportunity:function(){
            var self = this
            var filter_date = self._get_date()
            rpc.query({
              model: "crm.lead",
              method: "check_user_group",
              }).then(function(result){
              if (result == true){
                  self.do_action({
                      name:'My Opportunity',
                      type: 'ir.actions.act_window',
                      res_model: 'crm.lead',
                      view_mode: 'tree,form,calendar',
                      views: [[false, 'list'],[false, 'form']],
                      domain: [['type','=', 'opportunity'],['create_date', '>', filter_date['key1']], ['create_date', '<', filter_date['key2']]]
                  });
              }
              else{
                  self.do_action({
                      name:'My Opportunity',
                      type: 'ir.actions.act_window',
                      res_model: 'crm.lead',
                      view_mode: 'tree,form,calendar',
                      views: [[false, 'list'],[false, 'form']],
                      domain: [['user_id', '=', session.uid],['type','=', 'opportunity'],['create_date', '>', filter_date['key1']], ['create_date', '<', filter_date['key2']]],
                  });
              }
          })
          }
     })
  core.action_registry.add('crm_dashboard_tags', CustomDashBoard);
  return CustomDashBoard;
  })