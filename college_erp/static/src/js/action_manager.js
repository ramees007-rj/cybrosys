/** @odoo-module **/

import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import framework from 'web.framework';
import session from 'web.session';


registry.category("ir.actions.report handlers")
    .add("xlsx_handler", async function (action, options, env) {
   if (action.report_type === 'xlsx') {
       console.log('555')
       framework.blockUI();
       console.log('555')
       var def = $.Deferred();
       console.log('555')
       session.get_file({
           url: '/xlsx_reports',
           data: action.data,
           success: def.resolve.bind(def),
           complete: framework.unblockUI,
       });
       return def;
   }
})