    odoo.define('idle_timer.idle_timer', function (require) {
    'use strict';
    var SurveyFormWidget = require('survey.form');
    var _super_survey_form=SurveyFormWidget.prototype;
    var ajax = require('web.ajax');
//    console.log(_super_survey_form)
    SurveyFormWidget.include({
             init: function () {
                this._super.apply(this, arguments);
                },
        _qtimer: function (option,_submitForm) {
            var self = this;
            ajax.jsonRpc('/time_idle', 'call', {"method": 'record_recently_viewed_e', "args":{'token':this.options.surveyToken}}).then(function (data) {
                var iddletine = 0;
                var timelimit = 5;
                var timeinterval = "";
                timeinterval = setInterval(function () {
                  document.onmousemove = function () {
                       iddletine = 0;
                   }
                  iddletine += 1;
                  console.log(iddletine);
                  if (iddletine == timelimit) {
                    clearInterval(timeinterval);
                    timer()
                }
               },1000);
                function timer(){
                    var timer = data['question_time_limit']
                        var countDownDate
                        var add_minutes =  function (dt, minutes) {
                            return new Date(dt.getTime() + minutes*60000);
                            }
                          var countDownDate= add_minutes(new Date(), parseInt(timer));
                        var distance_seconds = countDownDate - new Date().getTime()
                        var x = setInterval(function() {
                          var now = new Date().getTime()
                          var distance = countDownDate - now;
                          var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                          var seconds = Math.floor((distance % (1000 * 60)) / 1000);
                            console.log(minutes + "m " + seconds + "s ");
                            document.getElementById('seconds').innerHTML = minutes + "m " + seconds + "s "
                          if (iddletine == 0 ){
                            clearInterval(x);
                          }
                          if (seconds < 50) {
                            self._submitForm(option)
                            clearInterval(x);

                          }
                        }, 1000);
                }
//                idle_timer = data['idle_time']
//                is_question_time_limit = data['is_question_time_limit']
//                question_time_limit = data['question_time_limit']
//                console.log(data['question_time_limit'])
                console.log(data)
            })
        },
        _initBreadcrumb: function (_submitForm) {
            var option = this.options
            this._super.apply(this, arguments);
            this._qtimer(option,_submitForm)
            document.getElementById('seconds').innerHTML = " "
        },
        _submitForm: function (options) {
            console.log(this.check_timer)
            this._super.apply(this, arguments);
        },
//        _hi:function(){
//            console.log('ss')
//        }


    });
//    PublicWidget.registry.SurveyTimerQ = Dynamic;
//    return Dynamic;
});

//odoo.define('quiz_idle_timer.timer', function (require) {
//"use strict";
//
//var publicWidget = require('web.public.widget');
//var SurveyFormWidget = require('survey.form');
//var rpc = require('web.rpc');
//
//
//SurveyFormWidget = SurveyFormWidget.include({
//    _initTimer: function (){
//                var line = this._super.apply(this, arguments);
//                this.inactivityTime();
//                return line
//        },
//    inactivityTime : function() {
//                var self = this;
//                let mouseIdleTime= 0
//                let warningCount= 0
//                let count = 0
//                rpc.query({
//                    route: '/time_idle',
//                    params: {},
//                })
//                },
//    });
//});