/** @odoo-module **/
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
import core from 'web.core';
import session from 'web.session';
import rpc from 'web.rpc';
//var Menu = require('web.Menu');
import config from 'web.config';
   /**
 * Menu item appended in the systray part of the navbar
 */
var ThemeMenu = Widget.extend({
    name: 'activity_menu',
    template: 'night_mode.systray.ThemeMenu',
    events: {
        'change .switch': '_ontoggleClick',
        'click .switch': '_onclicktheme',
    },
    start: function() {
        var self = this;
        return this._super().then(function() {
            rpc.query({
                model: 'res.users',
                method: 'get_active',
                args: [],
            }).then(function(result) {
                if (result) {
                    self._ontoggleClickTrue({});
                    $("#fa-icon").removeClass("fa fa-moon-o").addClass("fa fa-sun-o");
                }
                else{
                    $("#fa-icon").removeClass("fa fa-sun-o").addClass("fa fa-moon-o");
                }
                document.addEventListener("DOMContentLoaded", function() {
                document.getElementById('check').checked = result || false;
                console.log(result,'last')
                })

             });
        });
    },
    _onclicktheme:function(events){
        $('.toggle-switch').on('click', function() {
          if ( $('.toggle-switch').attr('checked', true) ) {
            $("#fa-icon").removeClass("fa fa-moon-o").removeClass("moon-color").addClass("fa fa-sun-o").addClass("sun-color");
          }
          else {
            $("#fa-icon").removeClass("sun-color").removeClass("fa fa-sun-o").addClass("fa fa-moon-o").addClass("moon-color");
          }
        });
     },
    _ontoggleClick: function(events) {
        var self = this;
        var toggle_value = document.getElementById('check').checked;
        if (toggle_value == true) {
            rpc.query({
                model: 'res.users',
                method: 'set_active',
                args: [],
            }).then(function(res) {
                if (res == true) {
                        self._ontoggleClickTrue({});
                }
            });
        } else if (toggle_value == false) {
            rpc.query({
                model: 'res.users',
                method: 'set_deactive',
                args: [],
            }).then(function(res) {
                location.reload();
                return res;
            });
        }
    },
    _ontoggleClickTrue:function(events){
        var script = document.querySelector('script');
        $('.o_graph .o_graph_container .o_graph_svg_container svg').css('background-color', '#3c3f41');
        $('.dropdown-menu ').css('background-color', '#3c3f41');
        var o_required_modifier = document.createElement('style');
        o_required_modifier.innerHTML =
         '.o_required_modifier.o_input,.o_required_modifier .o_input {' +
            'background-image: linear-gradient(to bottom, #adadad,#adadad 100%) !important;' +
            'color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_required_modifier, script);
        $('.o_base_settings .o_setting_container .settings > .app_settings_block h2').css('background-color', '#3c3f41');
        $('.o_base_settings .o_setting_container .settings > .app_settings_block h2').css('color', '#adadad');
        $('.o_base_settings .o_setting_container .settings').css('background-color', '#3c3f41');
        var oe_edit_only = document.createElement('style');
        oe_edit_only.innerHTML =
         '.o_kanban_view.o_kanban_dashboard .o_kanban_record .o_kanban_card_manage_pane.container div[class*="col-"] > .o_kanban_card_manage_title {' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(oe_edit_only, script);
        $('.app_settings_block').css('background-color', '#3c3f41');
        $('.o_loading').css('background-color', '#3c3f41');
        var oe_icon = document.createElement('style');
        oe_icon.innerHTML =
         '.o_dashboard .oe_dashboard .oe_action .oe_header .oe_icon {' +
            'color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(oe_icon, script);
        $(' .o_mail_preview ').css('background-color', '#3c3f41');
        $('.o_kanban_record').css('background-color', '#3c3f41');
        $('.o_kanban_record').css('color', '#adadad');
        $('a').css('color', '#adadad');
        var o_search_panel = document.createElement('style');
        o_search_panel.innerHTML =
         '.o_controller_with_searchpanel .o_search_panel {' +
         'background-color: #3c3f41 !important;' +
         'color: #adadad !important;' +
         '}'
         +
         '.o_search_panel_category_value {' +
         'background-color: #3c3f41 !important;' +
         'color: #adadad !important;' +
         '}'
         +
         '.o_search_panel .list-group-item .o_search_panel_label_title {' +
         'color: #adadad !important;' +
         '}'
         +
         'section header b{' +
         'color: #adadad !important;' +
         '}'
         ;
        script.parentNode.insertBefore(o_search_panel, script);
        $('.o_graph_controller .o_graph_renderer .o_graph_canvas_container canvas').css('color', '#3c3f41');

        var content_center = document.createElement('style');
        content_center.innerHTML =
         '.o_content .content_center {' +
         'background-color: #3c3f41 !important;' +
         'border-bottom: 1px solid #3c3f41 !important;' +
         'border-top: 1px solid #3c3f41 !important;' +
         'color: #adadad !important;' +
         '}'
        script.parentNode.insertBefore(content_center, script);
        $('.o_graph_controller .o_graph_renderer .o_graph_canvas_container canvas').css('color', '#3c3f41');
        $('.m-2').css('color', '#adadad');

//
//            var o_nocontent_help = document.createElement('style');
//            o_nocontent_help.innerHTML =
//             '.o_view_sample_data .o_nocontent_help {' +
//             'background-color: #3c3f41 !important;' +
//             'border-bottom: 1px solid #3c3f41 !important;' +
//             'border-top: 1px solid #3c3f41 !important;' +
//             'color: #adadad !important;' +
//             '}'
//            script.parentNode.insertBefore(o_nocontent_help, script);
//            $('.o_graph_controller .o_graph_renderer .o_graph_canvas_container canvas').css('color', '#3c3f41');


        var o_nocontent_help = document.createElement('style');
        o_nocontent_help.innerHTML =
         '.o_view_sample_data .o_nocontent_help {' +
         'background-color: #3c3f41 !important;' +
         'border-radius: 20%;'+
         'box-shadow: 0 0 120px 100px #3c3f41 !important;'+
         '}'
        script.parentNode.insertBefore(o_nocontent_help, script);
        $('.o_graph_controller .o_graph_renderer .o_graph_canvas_container canvas').css('color', '#3c3f41');


        var o_graph_controller = document.createElement('style');
        o_graph_controller.innerHTML =
         '.o_content .o_graph_controller .o_graph_renderer canvas{'
         +
         'background-color: #616a75 !important;'
         +
         '}' +
         '.o_graph_canvas_container canvas{' +
            'background-color: #aea57b !important;' +
            '}';
        script.parentNode.insertBefore(o_graph_controller,script);
        var indeterminate = document.createElement('style');
        indeterminate.innerHTML =
         '.custom-control.custom-checkbox .custom-control-input:not(:checked):not(:indeterminate) ~ .custom-control-label::before {' +
            'outline: 1px solid #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(indeterminate, script);
        $('.o_list_view tfoot').css('background-color', '#3c3f41');
        $('.o_list_view thead').css('background-color', '#3c3f41');
        var o_main_navbar_hover = document.createElement('style');
        o_main_navbar_hover.innerHTML =
          '.o_main_navbar > ul > li > a:hover {' +
            'background-color: #6b6b6b !important;' +
             '}';
        script.parentNode.insertBefore(o_main_navbar_hover, script);
        $('.table thead th').css('border-color', '#6b6b6b');
        $('.o_form_view .o_form_sheet_bg').css('border-color', '#6b6b6b');
        var o_theme_kanban = document.createElement('style');
        o_theme_kanban.innerHTML =
          '.o_kanban_view.o_theme_kanban {' +
            'background-color: #2a2a2a !important;' +
             '}';
        script.parentNode.insertBefore(o_theme_kanban, script);
        $('.o_column_sortable').css('border-color', '#6b6b6b');
        $('.select').css('background-color', '#3c3f41');
        var o_activity_view = document.createElement('style');
        o_activity_view.innerHTML =
          '.o_activity_view > table {' +
            'background-color: #3c3f41 !important;' +
            'color: #ada987 !important;' +
             '}';
        script.parentNode.insertBefore(o_activity_view, script);
        $('.o_form_view').css('background-color', '#3c3f41');
        $('.o_form_statusbar').css('background-color', '#3c3f41');
        var o_calendar_sidebar_container = document.createElement('style');
        o_calendar_sidebar_container.innerHTML =
          '.o_calendar_container .o_calendar_sidebar_container .ui-datepicker .ui-widget-header {' +
            'background-color: #3c3f41 !important;' +
            'color: #ada987 !important;' +
            'border-color:#7b7b7b !important;'+
             '}'
             +
             '.o_calendar_sidebar_container {' +
            'background-color: #3c3f41 !important;' +
             '}';
        script.parentNode.insertBefore(o_calendar_sidebar_container, script);
        $('.o_control_panel hr').css('border-color', '#6b6b6b');
        $('.o_content .o_form_view .o_form_sheet').css('border-color', '#6b6b6b');
        var o_datepicker = document.createElement('style');
        o_datepicker.innerHTML =
          '.ui-datepicker {' +
            'background-color: #6b6b6b !important;' +
             '}';
        script.parentNode.insertBefore(o_datepicker, script);
        $('nav.o_main_navbar').css('background-color', '#3c3f41');
        $('nav.o_main_navbar').css('border-bottom', '1px solid #6b6b6b');
        var oe_action = document.createElement('style');
        oe_action.innerHTML =
          '.o_dashboard .oe_dashboard .oe_action .oe_content {' +
            'background-color: #adadad !important;' +
             '}';
        script.parentNode.insertBefore(oe_action, script);
        $('.o_content').css('background-color', '#2a2a2a');
        $('.o_kanban_manage_toggle_button').css('color', '#adadad');
        $('.o_facet_values').css('color', '#adadad');
        var o_kanban_quick_create = document.createElement('style');
        o_kanban_quick_create.innerHTML =
          '.o_kanban_view .o_kanban_quick_create {' +
            'background-color: #adadad !important;' +
             '}';
        script.parentNode.insertBefore(o_kanban_quick_create, script);
        $('.breadcrumb').css('background-color', '#3c3f41');
        $('.o_control_panel > .breadcrumb').css('background-color', '#3c3f41');
        $('.o_field_widget .o_input_dropdown > input').css('background-color', '#3c3f41');
        var oe_header = document.createElement('style');
        oe_header.innerHTML =
          '.o_dashboard .oe_dashboard .oe_action .oe_header {' +
            'background-color: #adadad !important;' +
             '}';
        script.parentNode.insertBefore(oe_header, script);
        $('.o_calendar_container .o_calendar_sidebar_container .o_calendar_filter ').css('color', '#adadad');
        $('.o_calendar_container').css('background-color', '#3c3f41');
        var o_thread_window_header = document.createElement('style');
        o_thread_window_header.innerHTML =
          '.o_thread_window .o_thread_window_header {' +
            'background-color: #2a2a2a !important;' +
             'color: #afb1b3 !important;' +
             'border-bottom: 1px solid #afb1b3 !important;' +
             '}';
        script.parentNode.insertBefore(o_thread_window_header, script);
        $('.o_pivot table th ').css('color', '#adadad');
        $('.o_pivot table td ').css('color', '#adadad');
        $('.o_pivot table td ').css('background-color', '#3c3f41');
        var ace_content = document.createElement('style');
        ace_content.innerHTML =
          '.ace_content {' +
            'background-color: #adadad !important;' +
             '}';
        script.parentNode.insertBefore(ace_content, script);
        $('.dropdown-item-text ').css('color', '#adadad');
        $('.dropdown-menu ').css('border-color', '#6b6b6b');
        var o_note_input = document.createElement('style');
        o_note_input.innerHTML =
          '.o_note.o_mail_preview .o_note_input {' +
            'background-color: #adadad !important;' +
             '}';
        script.parentNode.insertBefore(o_note_input, script);
        $('.oe_module_action > .btn-secondary').css('color', '#43494a');
        $('.oe_module_action > .btn-info').css('color', '#43494a');
        var o_main_navbar_hover_active = document.createElement('style');
        o_main_navbar_hover_active.innerHTML =
           '.o_main_navbar > a:hover {' +
             'background-color: #6b6b6b !important;' +
             '}';
        script.parentNode.insertBefore(o_main_navbar_hover_active, script);
        $('.o_searchview .o_searchview_facet .o_searchview_facet_label ').css('background-color', '#43494a');
        $('.o_searchview .o_searchview_facet .o_searchview_facet_label ').css('border-color', '#4b4b4b');
        var o_arrow_button_stage = document.createElement('style');
        o_arrow_button_stage.innerHTML =
           '.o_form_view .o_form_statusbar > .o_statusbar_status > .o_arrow_button:not(:first-child):after {' +
             'border-left-color: #434849 !important;' +
             '}';
        script.parentNode.insertBefore(o_arrow_button_stage, script);
        $('.o_web_settings_dashboard_apps').css('background-color', '#3c3f41');
        $('.o_web_settings_dashboard_apps').css('color', '#adadad');
        var dropdown_hover = document.createElement('style');
        dropdown_hover.innerHTML =
          ' .dropdown-item:hover {' +
          'background-color: #6b6b6b !important;' +
           '}';
        script.parentNode.insertBefore(dropdown_hover, script);
        $('.breadcrumb ').css('background-color', '#3c3f41');
        $('.dropdown-item.active ').css('background-color', '#6b6b6b');
        var label_hover = document.createElement('style');
        label_hover.innerHTML =
          ' .o_main_navbar > ul > li > label:hover {' +
          'background-color: #6b6b6b !important;' +
           '}';
        script.parentNode.insertBefore(label_hover, script);
        $('.o_stat_text').css('color', '#adadad');
        $('.o_stat_text').css('background-color', '#3c3f41');
        var o_main_navbar_active = document.createElement('style');
        o_main_navbar_active.innerHTML =
        '.o_main_navbar > ul > li > a:focus, .o_main_navbar > ul > li > a:active, .o_main_navbar > ul > li > a:focus:active {' +
          'background-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_main_navbar_active, script);
        $('.o_composer').css('border-color', '#6b6b6b');
        $('.o_composer').css('background-color', '#2a2a2a');
        var o_group_header = document.createElement('style');
        o_group_header.innerHTML =
         '.o_list_view tbody > tr.o_group_header {' +
            'background-image: linear-gradient(to bottom, #adadad,#adadad 100%) !important;' +
            'color: #43494a !important;' +
            '}';
        script.parentNode.insertBefore(o_group_header, script);
        $('.o_thread_date').css('background-color', '#43494a');
        $('.o_mail_thread .o_thread_date_separator').css('border-bottom', '1px solid #2a2a2a');
        var o_mail_discuss = document.createElement('style');
        o_mail_discuss.innerHTML =
                '.o_mail_discuss .o_mail_discuss_content .o_mail_thread {' +
                'background-color: #2a2a2a !important;' +
                'color: #adadad !important;' +
                '}';
        script.parentNode.insertBefore(o_mail_discuss, script);
        $('.o_input_dropdown').css('background-color', '#3c3f41');
        $('.o_field_widget').css('background-color', '#3c3f41');

        var o_Discuss_content = document.createElement('style');
        o_Discuss_content.innerHTML =
                '.o_Discuss_content .o_MessageList.o-empty.o_ThreadView_messageList {' +
                'background-color: #2a2a2a !important;' +
                'color: #adadad !important;' +
                '}';
        script.parentNode.insertBefore(o_Discuss_content, script);
        $('.o_input_dropdown').css('background-color', '#3c3f41');
        $('.o_field_widget').css('background-color', '#3c3f41');

        var o_control_panel_breadcrumb = document.createElement('style');
        o_control_panel_breadcrumb.innerHTML =
                ' .o_control_panel > .breadcrumb {' +
                'background-color: #3c3f41 !important;' +
                '}';
        script.parentNode.insertBefore(o_control_panel_breadcrumb, script);
        $('.o_progressbar .o_progress').css('border-color', '#6b6b6b');
        $('.o_input').css('background-color', '#333638');
        var o_kanban_record = document.createElement('style');
        o_kanban_record.innerHTML =
            '.o_kanban_record{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_kanban_record, script);
        $('.o_form_view .o_form_statusbar > .o_statusbar_buttons').css('background-color', '#3c3f41');
        $('.o_form_view .o_group .o_td_label').css('border-color', '#6b6b6b');
        var a = document.createElement('style');
        a.innerHTML =
            'a {' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(a, script);
        $('.ui-state-focus').css('background-color', '#6b6b6b');
        $('.note-editor .note-editing-area .note-editable').css('background-color', '#b7b6b6');
        var o_column_sortable = document.createElement('style');
        o_column_sortable.innerHTML =
            '.o_column_sortable{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            'border-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_column_sortable, script);
        $('.o_field_widget.o_field_many2one .o_external_button ').css('background-color', '#3c3f41');
        $('html .o_web_client > .o_main .o_main_content .o_control_panel ').css('background-color', '#3c3f41');
        var o_kanban_grouped = document.createElement('style');
        o_kanban_grouped.innerHTML =
            '.o_kanban_view.o_event_kanban_view .o_kanban_record .o_event_left {' +
            'background-color: #43494a !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_kanban_grouped, script);
        $('.o_form_view .o_form_statusbar > .o_statusbar_status > .o_arrow_button.btn-primary.disabled ').css('color', '#adadad');
        $('.o_form_view .o_form_statusbar > .o_statusbar_status > .o_arrow_button.btn-primary.disabled ').css('background-color', '#3c3f41');
        var o_dropdown_kanban = document.createElement('style');
        o_dropdown_kanban.innerHTML =
            '.o_kanban_view .o_kanban_record .o_dropdown_kanban .dropdown-menu {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_dropdown_kanban, script);
        $('.o_event_left').css('color', '#afb1b3');
        $('.o_main_navbar .dropdown-menu').css('background-color', '#3c3f41');
        var o_kanban_grouped_view = document.createElement('style');
        o_kanban_grouped_view.innerHTML =
            '.o_kanban_view.o_kanban_grouped {' +
            'background-color: #292929 !important;' +
             'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_kanban_grouped_view, script);
        $('.btn-info').css('background-color', '#afb1b3');
        $('.btn-info').css('color', '#43494a');
        var o_dropdown_kanban_dashboard = document.createElement('style');
        o_dropdown_kanban_dashboard.innerHTML =
            '.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_manage_toggle_button {' +
            'background-color: #3c3f41 !important;' +
            'border-color: #4b4b4b !important;' +
            '}';
        script.parentNode.insertBefore(o_dropdown_kanban_dashboard, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_manage_toggle_button').css('background-color', '#3c3f41');
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_manage_toggle_button').css('border-color', '#4b4b4b');
        var dropdown_header = document.createElement('style');
        dropdown_header.innerHTML =
            '.dropdown-header{' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(dropdown_header, script);
        $('.o_column_sortable').css('background-color', '#3c3f41');
        $('.o_column_sortable').css('border-color', '#6b6b6b');
        var btn_info = document.createElement('style');
        btn_info.innerHTML =
            '.btn-info {' +
            'background-color: #afb1b3 !important;' +
            'border-color: #6b6b6b !important;' +
            'color: #43494a !important;' +
            '}';
        script.parentNode.insertBefore(btn_info, script);
        $('.o_kanban_record ').css('color', '#adadad');
        $('.o_kanban_record ').css('border-color', '#6b6b6b');
        var o_dropdown_open = document.createElement('style');
        o_dropdown_open.innerHTML =
            '.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_dropdown_open, script);
        $('.o_kanban_view.o_kanban_grouped').css('color', '#adadad');
        $('.oe_stat_button').css('background-color', '#3c3f41');
        var o_event_left = document.createElement('style');
        o_event_left.innerHTML =
            '.o_event_left {' +
            'background-color: #43494a !important;' +
            'color: #afb1b3 !important;' +
            '}';
        script.parentNode.insertBefore(o_event_left, script);
        $('.btn-primary').css('color', '#43494a');
        $('.o_control_panel o_breadcrumb_full').css('background-color', '#3c3f41');
        var o_list_view = document.createElement('style');
        o_list_view.innerHTML =
            '.o_list_view{' +
            'background-color: #3c3f41 !important;' +
             'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_list_view, script);
        $('.btn-secondary').css('border-color', '#6b6b6b');
        $('.btn-secondary').css('color', '#afb1b3');
        var o_list_view_tfoot = document.createElement('style');
        o_list_view_tfoot.innerHTML =
            '.o_list_view tfoot{' +
            'background-color: #3c3f41 !important;' +
             'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_list_view_tfoot, script);
        $('.o_form_view .o_form_statusbar').css('border-color', '#6b6b6b');
        $('.fc td').css('border-color', '#6b6b6b');
        var o_list_view_thead = document.createElement('style');
        o_list_view_thead.innerHTML =
            '.o_list_view thead , tbody {' +
            'background-color: #3c3f41 !important;' +
             'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_list_view_thead, script);
        $('.o_searchview').css('color', '#adadad');
        $('.o_pager_counter').css('color', '#adadad');
        var o_main_navbar = document.createElement('style');
        o_main_navbar.innerHTML =
            '.o_main_navbar .dropdown-menu{' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_main_navbar, script);
        $('.o_searchview .o_searchview_input_container .o_searchview_input').css('background-color', '#3c3f41');
        $('.o_searchview .o_searchview_input_container .o_searchview_input').css('color', '#adadad');
        var o_main_navbar_font = document.createElement('style');
        o_main_navbar_font.innerHTML =
            '.o_main_navbar .dropdown-item{' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_main_navbar_font, script);
        $('.o_dropdown_toggler_btn').css('background-color', '#3c3f41');
        $('.o_dropdown_toggler_btn').css('color', '#adadad');
        var table_th = document.createElement('style');
        table_th.innerHTML =
            '.table th,.table td {' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(table_th, script);
        $('.dropdown-item ').css('color', '#adadad');
        $('.dropdown-header ').css('color', '#adadad');
        var table_thead_th = document.createElement('style');
        table_thead_th.innerHTML =
            '.table thead th{' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(table_thead_th, script);
        $('.dropdown-menu ').css('color', '#adadad');
        $('.dropdown-menu ').css('border-color', '#6b6b6b');
        var o_column_sortable_border = document.createElement('style');
        o_column_sortable_border.innerHTML =
            '.o_column_sortable{' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_column_sortable_border, script);
        $('.o_web_settings_dashboard_share').css('background-color', '#3c3f41');
        $('.o_web_settings_dashboard_share').css('color', '#adadad');
        var btn_link = document.createElement('style');
        btn_link.innerHTML =
                    '.btn-link {' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(btn_link, script);
        $('.o_web_settings_dashboard_invitations').css('background-color', '#3c3f41');
        $('.o_web_settings_dashboard_invitations').css('color', '#adadad');
        var o_statusbar_status = document.createElement('style');
        o_statusbar_status.innerHTML =
                    '.o_form_view .o_form_statusbar > .o_statusbar_status > .o_arrow_button.btn-primary.disabled {' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_statusbar_status, script);
        $('.o_web_settings_dashboard_company').css('background-color', '#3c3f41');
        $('.o_web_settings_dashboard_company').css('color', '#adadad');
        var oe_kanban_card = document.createElement('style');
        oe_kanban_card.innerHTML =
                    '.o_kanban_view .oe_kanban_card .o_dropdown_kanban.show .dropdown-toggle, .o_kanban_view .o_kanban_record .o_dropdown_kanban.show .dropdown-toggle {' +
                    'background-color: #3c3f41 !important;' +
                    'border-color:  #3c3f41 !important;' +
                    '}';
        script.parentNode.insertBefore(oe_kanban_card, script);
        $('.o_web_settings_dashboard_translations').css('background-color', '#3c3f41');
        $('.o_web_settings_dashboard_translations').css('color', '#adadad');
        var o_content = document.createElement('style');
        o_content.innerHTML =
                    '.o_content .o_form_view .o_form_sheet, .modal-content .o_form_view .o_form_sheet{' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_content, script);
        $('.o_mail_thread').css('background-color', '#2a2a2a');
        $('.o_mail_thread').css('color', '#adadad');

        var container = document.createElement('style');
        container.innerHTML =
                    '.o_content .o_purchase_dashboard.container{' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(container, script);
        $('.o_mail_thread').css('background-color', '#2a2a2a');
        $('.o_mail_thread').css('color', '#adadad');

        var o_text = document.createElement('style');
        o_text.innerHTML =
                    '.o_content .o_purchase_dashboard.container .o_text{' +
                    'background-color: #2a2a2a !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_text, script);
        $('.o_mail_thread').css('background-color', '#2a2a2a');
        $('.o_mail_thread').css('color', '#adadad');

//            var o_purchase_dashboard = document.createElement('style');
//            o_purchase_dashboard.innerHTML =
//                        '.o_content .o_purchase_dashboard .table tbody > tr > td{' +
//                        'background-color: #2a2a2a !important;' +
//                        'color: #adadad !important;' +
//                        '}';
//            script.parentNode.insertBefore(o_purchase_dashboard, script);
//            $('.o_mail_thread').css('background-color', '#2a2a2a');
//            $('.o_mail_thread').css('color', '#adadad');

        var o_Discuss = document.createElement('style');
        o_Discuss.innerHTML =
                    '.o_Discuss .o_form_view .o_form_sheet, .modal-content .o_form_view .o_form_sheet{' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Discuss, script);
        $('.o_Discuss_content').css('background-color', '#3c3f41');
        $('.o_Discuss_content').css('color', '#adadad');
        $('.o_Discuss .o_Discuss_content .o_ThreadViewTopbar').css('background-color', '#3c3f41');
        $('.o_Discuss .o_DiscussSidebar').css('background-color', '#212529 !important;');
        $('.o_Discuss .o_DiscussSidebar').removeClass('bg-light');
        $('.o_Discuss .o_DiscussSidebar').removeClass('border-right');
        $('.o_Message').css('background-color', '#3c3f41 !important');

        var o_Discuss_thread = document.createElement('style');
        o_Discuss_thread.innerHTML =
                    '.o_Discuss .o_ThreadView.o_Discuss_thread {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Discuss_thread, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_progressbar = document.createElement('style');
        o_progressbar.innerHTML =
                    '.o_progressbar .o_progress {' +
                    'border-color: 1px solid #6b6b6b !important;' +
                    'background-color: #3c3f41 !important;' +
                    '}';
        script.parentNode.insertBefore(o_progressbar, script);
        $('.ui-autocomplete').css('background-color', '#3c3f41');
        $('.ui-autocomplete').css('border-color', '#6b6b6b');
        var o_progressbar_complete = document.createElement('style');
        o_progressbar_complete.innerHTML =
                    '.o_progressbar .o_progress .o_progressbar_complete {' +
                    'border: 1px solid #6b6b6b !important;' +
                    'background-color: #747677 !important;' +
                    '}';
        script.parentNode.insertBefore(o_progressbar_complete, script);
        $('.o_stock_reports_page').css('color', '#adadad');
        $('.o_field_widget.o_field_many2one .o_external_button ').css('color', '#adadad');
        var bottom_block = document.createElement('style');
        bottom_block.innerHTML =
                    '.o_kanban_view.o_kanban_dashboard .o_kanban_record .o_kanban_card_header + .container.o_kanban_card_content .o_kanban_primary_bottom.bottom_block {' +
                     'background-color: #242729 !important;' +
                     'border-top: 1px solid #6b6b6b !important;' +
                    '}';
        script.parentNode.insertBefore(bottom_block, script);
        $('.btn-link').css('color', '#adadad');
        $('.o_stock_reports_page').css('background-color', '#3c3f41');

        var o_Chatter_activityBox = document.createElement('style');
        o_Chatter_activityBox.innerHTML =
                    '.o_Chatter .o_ActivityBox.o_Chatter_activityBox {' +
                    'background-color: #2a2a2a !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Chatter_activityBox, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');

        var o_mail_not_discussion = document.createElement('style');
        o_mail_not_discussion.innerHTML =
                    '.o_mail_thread .o_thread_message.o_mail_not_discussion {' +
                    'background-color: #2a2a2a !important;' +
                    'border-bottom: 1px solid #6b6b6b !important;' +
                    '}';
        script.parentNode.insertBefore(o_mail_not_discussion, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');

        var o_Chatter_thread = document.createElement('style');
        o_Chatter_thread.innerHTML =
                    '.o_Chatter .o_ThreadView.o_Chatter_thread {' +
                    'background-color: #2a2a2a !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Chatter_thread, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');

        var o_ThreadView_messageList = document.createElement('style');
        o_ThreadView_messageList.innerHTML =
                    '.o_Chatter .o_MessageList.o_ThreadView_messageList {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_ThreadView_messageList, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_ThreadView_messageList = document.createElement('style');
        o_ThreadView_messageList.innerHTML =
                    '.o_Discuss_content .o_MessageList.o_ThreadView_messageList {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_ThreadView_messageList, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_Composer_toolButton = document.createElement('style');
        o_Composer_toolButton.innerHTML =
                    '.o_Discuss .o_Composer_button o_Composer_buttonEmojis o_Composer_toolButton {' +
                    'background-color: #2a2a2a !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Composer_toolButton, script);

        var o_MessageList_message = document.createElement('style');
        o_MessageList_message.innerHTML =
                    '.o_Chatter .o_Message.o-not-discussion.o-notification.o_MessageList_item.o_MessageList_message {' +
                    'background-color: #2a2a2a !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_MessageList_message, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_MessageList_message = document.createElement('style');
        o_MessageList_message.innerHTML =
                    '.o_Discuss .o_Message.o-discussion.o_MessageList_item.o_MessageList_message {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_MessageList_message, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');

        var o_MessageList_separatorDate = document.createElement('style');
        o_MessageList_separatorDate.innerHTML =
                    '.o_Discuss .o_MessageList_separator.o_MessageList_separatorDate.o_MessageList_item {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_MessageList_separatorDate, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_MessageList_separatorLabelDate = document.createElement('style');
        o_MessageList_separatorLabelDate.innerHTML =
                    '.o_Chatter .o_MessageList_separatorLabel.o_MessageList_separatorLabelDate {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_MessageList_separatorLabelDate, script);

        var o_MessageList_item = document.createElement('style');
        o_MessageList_item.innerHTML =
                    '.o_Chatter .o_MessageList_separator.o_MessageList_separatorDate.o_MessageList_item {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_MessageList_item, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');

        var o_MessageList_separatorLabelDate = document.createElement('style');
        o_MessageList_separatorLabelDate.innerHTML =
                    '.o_Discuss .o_MessageList_separatorLabel.o_MessageList_separatorLabelDate {' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_MessageList_separatorLabelDate, script);



        var o_ThreadView_composer = document.createElement('style');
        o_ThreadView_composer.innerHTML =
                    '.o_Discuss .o_Composer.o-has-current-partner-avatar.o-has-footer.o-is-compact.o_ThreadView_composer {' +
                    'background-color: #2a2a2a !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_ThreadView_composer, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_Composer_coreMain = document.createElement('style');
        o_Composer_coreMain.innerHTML =
                    '.o_Discuss .o_Composer_coreMain {' +
                    'background-color: #2a2a2a !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Composer_coreMain, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_ComposerTextInput_textarea = document.createElement('style');
        o_ComposerTextInput_textarea.innerHTML =
                    '.o_Discuss .o_ComposerTextInput_textarea {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_ComposerTextInput_textarea, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_Composer_toolButtons = document.createElement('style');
        o_Composer_toolButtons.innerHTML =
                    '.o_Discuss .o_Composer_toolButtons {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Composer_toolButtons, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_Composer_textInput = document.createElement('style');
        o_Composer_textInput.innerHTML =
                    '.o_Discuss .o_ComposerTextInput.o_Composer_textInput {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Composer_textInput, script);
        $('.o_kanban_view.o_kanban_dashboard .o_kanban_record.o_dropdown_open .o_kanban_card_manage_pane').css('background-color', '#3c3f41');
        $('.o_event_left').css('background-color', '#43494a');


        var o_kanban_ungrouped = document.createElement('style');
        o_kanban_ungrouped.innerHTML =
                    '.o_kanban_view.o_kanban_ungrouped .o_kanban_record {' +
                    'background-color: #3c3f41 !important;' +
                    '}';
        script.parentNode.insertBefore(o_kanban_ungrouped, script);
        $('.breadcrumb').css('border-color', '#3c3f41');
        $('.btn-info').css('border-color', '#6b6b6b');
        var html = document.createElement('style');
        html.innerHTML =
                    '.o_thread_window.o_thread_less .o_mail_thread {' +
                    'background-color: #3c3f41 !important;' +
                    '}';
        script.parentNode.insertBefore(html, script);
        $('.o_kanban_view.o_event_kanban_view .o_kanban_record .o_event_left').css('background-color', '#43494a');
        $('.o_kanban_view.o_event_kanban_view .o_kanban_record .o_event_left').css('color', '#adadad');
        $('.o_kanban_view .o_kanban_record .o_dropdown_kanban .dropdown-menu').css('background-color', '#3c3f41');
        var o_thread_search_input = document.createElement('style');
        o_thread_search_input.innerHTML =
                    '.o_thread_window.o_thread_less .o_thread_search_input {' +
                    'background-color: #3c3f41 !important;' +
                    'color: #afb1b3 !important;' +
                    '}';
        script.parentNode.insertBefore(o_thread_search_input, script);
        $('a ').css('color', '#adadad');
        $('.o_column_sortable').css('color', '#adadad');
        var o_thread_window = document.createElement('style');
        o_thread_window.innerHTML =
                    '.o_thread_window .o_mail_thread {' +
                    'background-color: #afb1b3 !important;' +
                    'color: #afb1b3 !important;' +
                    '}';
        script.parentNode.insertBefore(o_thread_window, script);
        $('.oe_stat_button').css('color', '#adadad');
        $('.oe_stat_button').css('border-color', '#6b6b6b');
        var o_mail_thread_content_input = document.createElement('style');
        o_mail_thread_content_input.innerHTML =
                    '.o_mail_thread .o_mail_thread_content, .o_mail_activity .o_mail_thread_content {' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_mail_thread_content_input, script);
        $('.o_control_panel.o_breadcrumb_full > .breadcrumb').css('background-color', '#3c3f41');
        $('.o_kanban_view.o_kanban_grouped').css('background-color', '#292929');
        var o_mail_thread_content_input_container = document.createElement('style');
        o_mail_thread_content_input_container.innerHTML =
                    '.o_thread_composer.o_chat_mini_composer .o_composer_container {' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_mail_thread_content_input_container, script);
        $('.btn-primary').css('background-color', '#afb1b3');
        $('.btn-primary').css('border-color', '#6b6b6b');
        var input = document.createElement('style');
        input.innerHTML =
                    '.o_thread_window.o_thread_less .o_thread_search_input > input {' +
                    'background-color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(input, script);
        $('.o_dropdown_toggler_btn').css('border-color', '#6b6b6b');
        $('.btn-secondary').css('background-color', '#434849');
        var o_control_panel = document.createElement('style');
        o_control_panel.innerHTML =
                    '.o_control_panel.o_breadcrumb_full > .breadcrumb {' +
                    'background-color: #3c3f41 !important;' +
                    '}';
        script.parentNode.insertBefore(o_control_panel, script);
        $('.o_searchview').css('background-color', '#3c3f41');
        $('.o_searchview').css('border-color', '#6b6b6b');
        var o_stock_reports_page = document.createElement('style');
        o_stock_reports_page.innerHTML =
                    '.o_stock_reports_page {' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_stock_reports_page, script);
        $('.o_searchview_more').css('background-color', '#3c3f41');
        $('.o_searchview_more').css('color', '#adadad');
        $('.o_searchview .o_searchview_facet').css('background-color', '#3c3f41');
        var o_external_button = document.createElement('style');
        o_external_button.innerHTML =
                    '.o_field_widget.o_field_many2one .o_external_button {' +
                    'background-color: #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_external_button, script);
        $('.dropdown-divider ').css('border-color', '#6b6b6b');
        $('.o_form_view .o_form_label').css('color', '#adadad');
        var o_main_content = document.createElement('style');
        o_main_content.innerHTML =
                    'html .o_web_client .o_control_panel {' +
                    'background-color: #3c3f41 !important;' +
                    '} '+ 'html .o_web_client > .o_action_manager > .o_action .o_content {' +
                    'background-color: #3c3f41 !important;' +
                    '}';
        script.parentNode.insertBefore(o_main_content, script);
        $('.o_list_view thead').css('color', '#adadad');
        $('.o_list_view').css('background-color', '#3c3f41');
        var autocomplete = document.createElement('style');
        autocomplete.innerHTML =
            '.ui-autocomplete {' +
            'background-color: #3c3f41 !important;' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(autocomplete, script);
        $('.table td ').css('border-color', '#6b6b6b');
        $('.o_list_view').css('color', '#adadad');
        $('.o_list_view tfoot').css('color', '#adadad');
        var o_list_table = document.createElement('style');
        o_list_table.innerHTML =
            '.o_list_view .o_list_table {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_list_table, script)
        $('.table tbody').css('background-color', '#3c3f41');
        var ui_state_focus = document.createElement('style');
        ui_state_focus.innerHTML =
            '.ui-state-focus {' +
            'background-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(ui_state_focus, script);
        $('.o_form_view .oe_chatter').css('background-color', '#3c3f41');
        $('.o_column_sortable').css('color', '#adadad');
        $('.o_column_sortable').css('background-color', '#3c3f41');
        var note_editor = document.createElement('style');
        note_editor.innerHTML =
            '.note-editor .note-editing-area .note-editable {' +
            'background-color: #747677 !important;' +
            '}';
        script.parentNode.insertBefore(note_editor, script);
        $('.o_control_panel').css('background-color', '#3c3f41');
        $('.o_control_panel').css('border-bottom', '1px solid #6b6b6b');
        $('.o_form_view .o_form_sheet_bg').css('background-image', 'url()');
        var o_badge_text = document.createElement('style');
        o_badge_text.innerHTML =
            '.o_field_widget.o_field_many2manytags .badge .o_badge_text {' +
            'color: #fff !important;' +
            '}';
        script.parentNode.insertBefore(o_badge_text, script);
        $('.o_kanban_view .o_kanban_record').css('border-color', '#6b6b6b');
        $('.nav-tabs .nav-link.active').css('background-color', '#3c3f41');
        var o_field_many2manytags = document.createElement('style');
        o_field_many2manytags.innerHTML =
            '.o_field_widget.o_field_many2manytags .badge {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_field_many2manytags, script);
        $('.o_calendar_container .o_calendar_view .o_calendar_widget *').css('color', '#adadad');
        $('.o_calendar_container .o_calendar_view .o_calendar_widget *').css('background-color', '#3c3f41');
        $('.o_calendar_container .o_calendar_sidebar_container .o_calendar_filter ').css('background-color', '#3c3f41');
        var o_field_datepicker = document.createElement('style');
        o_field_datepicker.innerHTML =
            '.o_calendar_container .o_calendar_sidebar_container .ui-datepicker table td {' +
            'background-color:#3c3f41 !important;' +
            'opacity: 1 !important;' +
            '}';
        script.parentNode.insertBefore(o_field_datepicker, script);
        $('.o_calendar_container ').css('background-color', '#3c3f41');
        $('.o_calendar_filter ').css('background-color', '#3c3f41');
        $('.o_pivot table th ').css('background-color', '#3c3f41');
        var o_field_datepicker_table = document.createElement('style');
        o_field_datepicker_table.innerHTML =
            '.o_calendar_container .o_calendar_sidebar_container .ui-datepicker table .ui-state-active {' +
            'background-color:#53b939 !important;' +
            'color: white !important;' +
            '}';
        script.parentNode.insertBefore(o_field_datepicker_table, script);
        $('.dropdown-menu.show ').css('background-color', '#43494a');
        $('.dropdown-menu.show ').css('color', '#adadad');
        $('.dropdown-item ').css('color', '#adadad');
        var o_field_widget_header = document.createElement('style');
        o_field_widget_header.innerHTML =
            '.o_calendar_container .o_calendar_sidebar_container .ui-datepicker table td a {' +
            'background-color:#3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_field_widget_header, script);
        $('.o_mail_preview:not(:last-child)').css('border-bottom', '#6b6b6b');
        $('.o_searchview_facet ').css('background-color', '#43494a');
        $('.o_searchview_facet ').css('color', '#adadad');
        var o_hr_attendance_kiosk_backdrop = document.createElement('style');
        o_hr_attendance_kiosk_backdrop.innerHTML =
            '.o_hr_attendance_kiosk_backdrop {' +
            'background-color: #2a2a2a !important;' +
            '}';
        script.parentNode.insertBefore(o_hr_attendance_kiosk_backdrop, script);
        $('select ').css('background-color', '#6b6b6b');
        $('select ').css('color', '#adadad');
        var o_hr_attendance_kiosk_mode = document.createElement('style');
        o_hr_attendance_kiosk_mode.innerHTML =
            '.o_hr_attendance_kiosk_mode {' +
            'background-color: #1e1f20 !important;' +
            '}';
        script.parentNode.insertBefore(o_hr_attendance_kiosk_mode, script);
        $('.o_form_view .o_horizontal_separator').css('color', '#adadad');
        $('.o_web_settings_dashboard').css('background-color', '#24272a');
        var o_hr_attendance_user_badge = document.createElement('style');
        o_hr_attendance_user_badge.innerHTML =
            '.o_hr_attendance_kiosk_mode .o_hr_attendance_user_badge {' +
            'background-color: #232426 !important;' +
            '}';
        script.parentNode.insertBefore(o_hr_attendance_user_badge, script);
        $('.oe_stat_button,.o_stat_value').css('color', '#adadad');
        $('.o_form_view .oe_button_box .oe_stat_button .o_button_icon').css('color', '#adadad');
        var o_hr_warning = document.createElement('style');
        o_hr_warning.innerHTML =
            '.btn-warning  {' +
            'background-color: #747677 !important;' +
            '}';
        script.parentNode.insertBefore(o_hr_warning, script);
        $('.o_thread_composer').css('border-color', '#6b6b6b');
        $('.oe_stat_button,.o_stat_value').css('background-color', '#3c3f41');
        var o_base_settings = document.createElement('style');
        o_base_settings.innerHTML =
            '.o_base_settings .o_setting_container .settings {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_base_settings, script);
        $('.o_thread_date').css('color', '#adadad');
        $('.o_thread_composer').css('background-color', '#2a2a2a');
        var o_setting_container = document.createElement('style');
        o_setting_container.innerHTML =
            '.o_base_settings .o_setting_container .settings > .app_settings_block h2 {' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_setting_container, script);
        $('.o_input_dropdown').css('color', '#adadad');
        $('.o_field_widget').css('color', '#adadad');
        var o_setting_search = document.createElement('style');
        o_setting_search.innerHTML =
            '.o_base_settings .o_control_panel .o_panel .o_setting_search .searchInput {' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_setting_search, script);
        $('.o_input').css('border-color', '#6b6b6b');
        $('.o_input').css('color', '#adadad');
        var o_form_statusbar_button = document.createElement('style');
        o_form_statusbar_button.innerHTML =
            '.o_form_view .o_form_statusbar > .o_statusbar_buttons {' +
             'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_form_statusbar_button, script);
        $('.o_base_settings .o_control_panel .o_panel .o_setting_search .searchInput').css('background-color', '#3c3f41');
        $('.o_base_settings .o_control_panel .o_panel .o_setting_search .searchInput').css('color', '#adadad');
        $('.o_form_view .o_group.o_inner_group.oe_subtotal_footer .oe_subtotal_footer_separator ').css('border-top', '1px solid #6b6b6b');
        var o_form_sheet_bg = document.createElement('style');
        o_form_sheet_bg.innerHTML =
            '.o_form_view .o_form_sheet_bg {' +
            'background-image: None !important;' +
            'border-color: #6b6b6b !important;' +
            'background-color: #292929 !important;' +
            '}';
        script.parentNode.insertBefore(o_form_sheet_bg, script);
        var o_form_view_o_group_border_color = document.createElement('style');
        o_form_view_o_group_border_color.innerHTML =
            '.o_form_view .o_group .o_td_label {' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_form_view_o_group_border_color, script);
        var o_form_view_border_color = document.createElement('style');
        o_form_view_border_color.innerHTML =
            '.o_content .o_form_view .o_form_sheet {' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_form_view_border_color, script);
        var oe_chatter = document.createElement('style');
        oe_chatter.innerHTML =
            '.o_form_view .oe_chatter {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(oe_chatter, script);
        var nav_tabs = document.createElement('style');
        nav_tabs.innerHTML =
            '.nav-tabs .nav-link.active {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(nav_tabs, script);
        var nav_link = document.createElement('style');
        nav_link.innerHTML =
            '.nav-tabs .nav-link {' +
            'border-bottom: none !important;' +
            '}';
        script.parentNode.insertBefore(nav_link, script);
        var o_form_view = document.createElement('style');
        o_form_view.innerHTML =
            '.o_form_view {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_form_view, script);
        var o_form_statusbar = document.createElement('style');
        o_form_statusbar.innerHTML =
            '.o_form_view .o_form_statusbar {' +
            'background-color: #3c3f41 !important;' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_form_statusbar, script);
        var oe_subtotal_footer_separator = document.createElement('style');
        oe_subtotal_footer_separator.innerHTML =
            '.o_form_view .o_group.o_inner_group.oe_subtotal_footer .oe_subtotal_footer_separator {' +
            'border-top: 1px solid #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(oe_subtotal_footer_separator, script);
        var o_input = document.createElement('style');
        o_input.innerHTML =
            '.o_input {' +
            'background-color: #333638 !important;' +
             'border-color: #6b6b6b !important;' +
             'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_input, script);
        var o_input_dropdown = document.createElement('style');
        o_input_dropdown.innerHTML =
            '.o_input_dropdown {' +
            'background-color: #3c3f41 !important;' +
             'color: #adadad !important;' +
            '}';

        script.parentNode.insertBefore(o_input_dropdown, script);
        var o_field_widget = document.createElement('style');
        o_field_widget.innerHTML =
            '.o_field_widget {' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_field_widget, script);
        var oe_stat_button = document.createElement('style');
        oe_stat_button.innerHTML =
            '.oe_stat_button {' +
            'background-color: #3c3f41 !important;' +
            'border-color: #6b6b6b !important;' +
            '}';

        script.parentNode.insertBefore(oe_stat_button, script);
        var modal_footer = document.createElement('style');
        modal_footer.innerHTML =
            '.modal-footer {' +
            'background-color: #3c3f41 !important;' +
            'border-top: #2a2a2a !important;' +
            '}';
        script.parentNode.insertBefore(modal_footer, script);
        var modal_header = document.createElement('style');
        modal_header.innerHTML =
            '.modal-header {' +
            'background-color: #3c3f41 !important;' +
             'border-bottom: #2a2a2a !important;' +
             'color: #adadad !important;' +
            '}'
        script.parentNode.insertBefore(modal_header, script);
        var o_thread_date = document.createElement('style');
        o_thread_date.innerHTML =
            '.o_thread_date {' +
            'background-color: #43494a !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_thread_date, script);
        var o_thread_date_separator = document.createElement('style');
        o_thread_date_separator.innerHTML =
            '.o_mail_thread .o_thread_date_separator {' +
            'border-bottom: 1px solid #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_thread_date_separator, script);
        var modal_body_form = document.createElement('style');
        modal_body_form.innerHTML =
            '.modal-body .o_form_view {' +
            'background-color: #282828 !important;' +
            '}';
        script.parentNode.insertBefore(modal_body_form, script);
        var modal_content_form = document.createElement('style');
        modal_content_form.innerHTML =
            '.modal-content .modal-body .o_form_view .o_form_sheet {'+
            'background-color: #292929 !important;'+
            'color: #adadad !important;'+
            '}';
        script.parentNode.insertBefore(modal_content_form, script);
        var modal_body = document.createElement('style');
        modal_body.innerHTML =
            '.modal-body {' +
            'background-color: #292929 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(modal_body, script);
        var modal_body_field_widget = document.createElement('style');
        modal_body_field_widget.innerHTML =
            '.modal-body .o_field_widget {' +
            'background-color: #282828 !important;' +
            '}';
        script.parentNode.insertBefore(modal_body_field_widget, script);
        var o_thread_composer = document.createElement('style');
        o_thread_composer.innerHTML =
            '.o_thread_composer {' +
            'background-color: #2a2a2a !important;' +
             'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_thread_composer, script);
        var o_composer = document.createElement('style');
        o_composer.innerHTML =
            '.o_composer {' +
            'background-color: #2a2a2a !important;' +
             'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_composer, script);

        var o_Chatter_topbar = document.createElement('style');
        o_Chatter_topbar.innerHTML =
                    '.o_Chatter .o_ChatterTopbar.o_Chatter_topbar {' +
                    'background-color: #3c3f41 !important;' +
                    'border-bottom: 1px solid #3c3f41 !important;' +
                    'border-top: 1px solid #3c3f41 !important;' +
                    'color: #adadad !important;' +
                    '}';
        script.parentNode.insertBefore(o_Chatter_topbar, script);

        var o_chatter_composer_active = document.createElement('style');
        o_chatter_composer_active.innerHTML =
            '.o_chatter.o_chatter_composer_active .o_chatter_topbar > .btn.o_active {' +
             'background-color: #2a2a2a !important;' +
            '}';
        script.parentNode.insertBefore(o_chatter_composer_active, script);
        var oe_stat_button_font = document.createElement('style');
        oe_stat_button_font.innerHTML =
            '.oe_stat_button,.o_stat_value {' +
            'color: #adadad !important;' +
            'background-color: #3c3f41 !important;' +
            '}';

        script.parentNode.insertBefore(oe_stat_button_font, script);
        var o_stat_text = document.createElement('style');
        o_stat_text.innerHTML =
            '.o_stat_text {' +
            'color: #adadad !important;' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_stat_text, script);
        var o_form_label = document.createElement('style');
        o_form_label.innerHTML =
            '.o_form_view .o_form_label {' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_form_label, script);
        var o_button_icon = document.createElement('style');
        o_button_icon.innerHTML =
            '.o_form_view .oe_button_box .oe_stat_button .o_button_icon {' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_button_icon, script);
        var o_horizontal_separator = document.createElement('style');
        o_horizontal_separator.innerHTML =
            '.o_form_view .o_horizontal_separator {' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_horizontal_separator, script);
        var o_web_settings_dashboard_apps = document.createElement('style');
        o_web_settings_dashboard_apps.innerHTML =
            '.o_web_settings_dashboard_apps{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_web_settings_dashboard_apps, script);
        var o_web_settings_dashboard_translations = document.createElement('style');
        o_web_settings_dashboard_translations.innerHTML =
            '.o_web_settings_dashboard_translations{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_web_settings_dashboard_translations, script);
        var o_web_settings_dashboard_company = document.createElement('style');
        o_web_settings_dashboard_company.innerHTML =
            '.o_web_settings_dashboard_company{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_web_settings_dashboard_company, script);
        var o_web_settings_dashboard_invitations = document.createElement('style');
        o_web_settings_dashboard_invitations.innerHTML =
            '.o_web_settings_dashboard_invitations{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_web_settings_dashboard_invitations, script);
        var o_web_settings_dashboard_share = document.createElement('style');
        o_web_settings_dashboard_share.innerHTML =
            '.o_web_settings_dashboard_share{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_web_settings_dashboard_share, script);
        var o_web_settings_dashboard = document.createElement('style');
        o_web_settings_dashboard.innerHTML =
            '.o_web_settings_dashboard{' +
            'background-color: #24272a !important;' +
            '}';
        script.parentNode.insertBefore(o_web_settings_dashboard, script);
        var o_graph_container = document.createElement('style');
            o_graph_container.innerHTML =
            '.o_graph .o_graph_container .o_graph_svg_container svg {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_graph_container, script);
        var o_main_navbar_hover_a = document.createElement('style');
        o_main_navbar_hover_a.innerHTML =
            '.o_main_navbar > ul > li > a:hover {' +
            'background-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_main_navbar_hover, script);
        var o_kanban_card_manage_title = document.createElement('style');
        o_kanban_card_manage_title.innerHTML =
            '.o_kanban_view.o_kanban_dashboard .o_kanban_record .o_kanban_card_manage_pane.container div[class*="col-"] > div:not(.o_kanban_card_manage_title) > a:hover {' +
            'background-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(o_kanban_card_manage_title, script);
        var dropdown_hover_item = document.createElement('style');
        dropdown_hover_item.innerHTML =
        ' .dropdown-item:hover {' +
        'background-color: #6b6b6b !important;' +
        '}';
        script.parentNode.insertBefore(dropdown_hover_item, script);
        var breadcrumb = document.createElement('style');
        breadcrumb.innerHTML =
        ' .breadcrumb {' +
        'background-color: #3c3f41 !important;' +
        '}';
        script.parentNode.insertBefore(breadcrumb, script);
        var o_datepicker_button = document.createElement('style');
        o_datepicker_button.innerHTML =
        '.o_datepicker .o_datepicker_button {' +
        'color: #000 !important;' +
        '}';
        script.parentNode.insertBefore(o_datepicker_button, script);
        var o_dropdown_button = document.createElement('style');
        o_dropdown_button.innerHTML =
        '.o_field_widget .o_input_dropdown .o_dropdown_button {' +
        'color: #000 !important;' +
        '}';
        script.parentNode.insertBefore(o_dropdown_button, script);
        var o_quick_create_unfolded = document.createElement('style');
        o_quick_create_unfolded.innerHTML =
        '.o_kanban_view .o_column_quick_create .o_quick_create_unfolded {' +
        'background-color: #3c3f41 !important;' +
        '}';
        script.parentNode.insertBefore(o_quick_create_unfolded, script);
        var o_column_folded = document.createElement('style');
        o_column_folded.innerHTML =
        '.o_kanban_view .o_kanban_group.o_column_folded {' +
        'background-color: #adadad !important;' +
        'color: #3c3f41 !important;' +
        '}';
        script.parentNode.insertBefore(o_column_folded, script);
        var dropdown_hover_active = document.createElement('style');
        dropdown_hover_active.innerHTML =
        ' .dropdown-item.active {' +
        'background-color: #6b6b6b !important;' +
        '}';
        script.parentNode.insertBefore(dropdown_hover_active, script);
        var select = document.createElement('style');
        select.innerHTML =
        ' select {' +
        'background-color: #6b6b6b !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(select, script);
        var o_mail_systray_item = document.createElement('style');
        o_mail_systray_item.innerHTML =
        ' .o_mail_preview {' +
        'background-color: #3c3f41 !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_mail_systray_item, script);
        var o_mail_systray_item_font = document.createElement('style');
        o_mail_systray_item_font.innerHTML =
        '.o_mail_systray_item .o_mail_systray_dropdown .o_mail_systray_dropdown_items .o_mail_preview {' +
        'color: #adadad !important;' +
        'background-color: #3c3f41 !important;' +
        '}';
        script.parentNode.insertBefore(o_mail_systray_item_font, script);
        var o_mail_systray_item_border = document.createElement('style');
        o_mail_systray_item_border.innerHTML =
        '.o_mail_systray_item .o_mail_systray_dropdown .o_mail_systray_dropdown_top  {' +
        'border-bottom: #6b6b6b !important;' +
        '}';
        script.parentNode.insertBefore(o_mail_systray_item_border, script);
        var o_mail_preview_item_border = document.createElement('style');
        o_mail_preview_item_border.innerHTML =
        '.o_mail_preview:not(:last-child) {' +
        'border-bottom: #6b6b6b !important;' +
        '}';
        script.parentNode.insertBefore(o_mail_preview_item_border, script);
        var o_searchview_input = document.createElement('style');
        o_searchview_input.innerHTML =
        ' .o_searchview .o_searchview_input_container .o_searchview_input {' +
        'background-color: #43494a !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_searchview_input, script);
        var o_searchview = document.createElement('style');
        o_searchview.innerHTML =
        ' .o_searchview {' +
        'background-color: #43494a !important;' +
        'border-color: #4b4b4b !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_searchview, script);
        var o_searchview_facet_label = document.createElement('style');
        o_searchview_facet_label.innerHTML =
        ' .o_searchview .o_searchview_facet .o_searchview_facet_label {' +
        'background-color: #43494a !important;' +
        'border-color: #4b4b4b !important;' +
        '}';
        script.parentNode.insertBefore(o_searchview_facet_label, script);
        var o_arrow_button = document.createElement('style');
        o_arrow_button.innerHTML =
            '.o_onboarding .o_onboarding_wrap{' +
            'background-color: rgba(76, 76, 76, 0.75) !important;'+
            'background-image: -webkit-gradient(linear, left top, left bottom, from(rgba(76, 76, 76, 0.5)), to(#272727)) !important;'+
            'background-image: -webkit-linear-gradient(top, rgba(76, 76, 76, 0.5), #272727) !important;'+
            'background-image: -moz-linear-gradient(top, rgba(76, 76, 76, 0.5), #272727) !important;'+
            'background-image: -ms-linear-gradient(top, rgba(76, 76, 76, 0.5), #272727) !important;'+
            'background-image: -o-linear-gradient(top, rgba(76, 76, 76, 0.5), #272727) !important;'+
            'background-image: linear-gradient(to bottom, rgba(76, 76, 76, 0.5), #272727) !important;'+
            'box-shadow: inset 0 -7px 20px -5px rgba(0, 0, 0, 0.3);' +
            '}';
        script.parentNode.insertBefore(o_arrow_button, script);
        var o_pager_counter = document.createElement('style');
        o_pager_counter.innerHTML =
        '.o_control_panel > .o_cp_right > .o_cp_pager .o_pager_counter {' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_pager_counter, script);
        var o_searchview_more = document.createElement('style');
        o_searchview_more.innerHTML =
        ' .o_searchview_more {' +
        'background-color: #43494a !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_searchview_more, script);
        var o_searchview_facet = document.createElement('style');
        o_searchview_facet.innerHTML =
        ' .o_searchview_facet {' +
        'background-color: #43494a !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_searchview_facet, script);
        var show_dropdown_menu = document.createElement('style');
        show_dropdown_menu.innerHTML =
        ' .dropdown-menu.show {' +
            'background-color: #43494a !important;' +
            'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(show_dropdown_menu, script);
        var show_dropdown_item_color = document.createElement('style');
        show_dropdown_item_color.innerHTML =
        ' .dropdown-item{ ' +
            'color: #adadad !important;' +
            'background-color: #43494a !important;' +
        '}';
        script.parentNode.insertBefore(show_dropdown_item_color, script);
        var show_dropdown_header_color = document.createElement('style');
        show_dropdown_header_color.innerHTML =
        ' .dropdown-header{ ' +
            'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(show_dropdown_header_color, script);
        var show_dropdown_item_text_color = document.createElement('style');
        show_dropdown_item_text_color.innerHTML =
        ' .dropdown-item-text{ ' +
            'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(show_dropdown_item_text_color, script);
        var dropdown_menu = document.createElement('style');
        dropdown_menu.innerHTML =
            '.dropdown-menu{' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(dropdown_menu, script);
        var dropdown_divider = document.createElement('style');
        dropdown_divider.innerHTML =
            '.dropdown-divider{' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(dropdown_divider, script);
        var o_mrp_bom_report_page = document.createElement('style');
        o_mrp_bom_report_page.innerHTML =
            '.o_mrp_bom_report_page {' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_mrp_bom_report_page, script);
        var btn_secondary = document.createElement('style');
        btn_secondary.innerHTML =
            '.btn-secondary {' +
            'background-color: #434849 !important;' +
            'border-color: #6b6b6b !important;' +
            'color: #afb1b3 !important;' +
            '}';
        script.parentNode.insertBefore(btn_secondary, script);
        var btn_primary = document.createElement('style');
        btn_primary.innerHTML =
            '.btn-primary {' +
            'background-color: #afb1b3 !important;' +
            'border-color: #6b6b6b !important;' +
            'color: #43494a !important;' +
            '}';
        script.parentNode.insertBefore(btn_primary, script);
        var o_pivot_table_th = document.createElement('style');
        o_pivot_table_th.innerHTML =
        '.o_pivot table th {' +
        'background-color: #3c3f41 !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_pivot_table_th, script);
        var o_pivot_table_td = document.createElement('style');
        o_pivot_table_td.innerHTML =
        '.o_pivot table td {' +
        'background-color: #3c3f41 !important;' +
        'color: #adadad !important;' +
        '}';
        script.parentNode.insertBefore(o_pivot_table_td, script);
        var o_calendar_widget = document.createElement('style');
        o_calendar_widget.innerHTML =
            '.o_calendar_container .o_calendar_view .o_calendar_widget *{' +
            'background-color: #3c3f41 !important;' +
            'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_calendar_widget, script);
        var o_field_widget_input = document.createElement('style');
        o_field_widget_input.innerHTML =
            '.o_field_widget .o_input_dropdown > input {' +
            'background-color: #3c3f41 !important;' +
            '}';
        script.parentNode.insertBefore(o_field_widget_input, script);
        var td = document.createElement('style');
        td.innerHTML =
            '.fc th,.fc td {' +
            'border-color: #6b6b6b !important;' +
            '}';
        script.parentNode.insertBefore(td, script);
        var o_calendar_filter = document.createElement('style');
        o_calendar_filter.innerHTML =
            '.o_calendar_container .o_calendar_sidebar_container .o_calendar_filter{' +
            'background-color: #3c3f41 !important;' +
             'color: #adadad !important;' +
            '}';
        script.parentNode.insertBefore(o_calendar_filter, script);
    },
});
SystrayMenu.Items.push(ThemeMenu);
export default ThemeMenu;