from odoo import models, fields, api
import re, ast


class InheritFinancialReport(models.TransientModel):
    _inherit = 'financial.report'

    team_id = fields.Many2one('crm.team', string='Sales Team')
    user_id = fields.Many2one('res.users', string='Team Member', domain=[])

    @api.onchange('team_id')
    def _onchange_team_id(self):
        domain = {'domain': {
            'user_id': [('id', 'in', self.team_id.member_ids.mapped('id'))]
        }}
        return domain

    def view_report_pdf(self):
        """This function will be executed when we click the view button
        from the wizard. Based on the values provided in the wizard, this
        function will print pdf report"""
        self.ensure_one()
        data = dict()
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(
            ['date_from', 'enable_filter', 'debit_credit', 'date_to',
             'account_report_id', 'target_move', 'view_format',
             'company_id', 'user_id', 'team_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(
            used_context,
            lang=self.env.context.get('lang') or 'en_US')

        report_lines = self.get_account_lines(data['form'])
        # find the journal items of these accounts
        journal_items = self.find_journal_items(report_lines, data['form'])

        def set_report_level(rec):
            """This function is used to set the level of each item.
            This level will be used to set the alignment in the dynamic reports."""
            level = 1
            if not rec['parent']:
                return level
            else:
                for line in report_lines:
                    key = 'a_id' if line['type'] == 'account' else 'id'
                    if line[key] == rec['parent']:
                        return level + set_report_level(line)

        # finding the root
        for item in report_lines:
            item['balance'] = round(item['balance'], 2)
            if not item['parent']:
                item['level'] = 1
                parent = item
                report_name = item['name']
                id = item['id']
                report_id = item['r_id']
            else:
                item['level'] = set_report_level(item)
        currency = self._get_currency()
        data['currency'] = currency
        data['journal_items'] = journal_items
        data['report_lines'] = report_lines
        print("journal_items", journal_items)
        print("report_lines", report_lines)
        # checking view type
        return self.env.ref(
            'base_accounting_kit.financial_report_pdf').report_action(self,
                                                                      data)

    def find_journal_items(self, report_lines, form):
        print("function_called")
        cr = self.env.cr
        journal_items = []
        for i in report_lines:
            print("i", i)
            if i['type'] == 'account':
                account = i['account']
                if form['target_move'] == 'posted':
                    print("target_move")
                    search_query = "select aml.id, am.id as j_id, aml.account_id, aml.date," \
                                   " aml.name as label, am.name," \
                                   + "(aml.debit-aml.credit) as balance, aml.debit, aml.credit, aml.partner_id, aml.user_id as team_member" \
                                   + " from account_move_line aml" \
                                     " join account_move am " \
                                     "on (aml.move_id=am.id and am.state=%s) " \
                                   + " where aml.account_id=%s"
                    vals = [form['target_move']]
                    # select aml.id, am.id as j_id, aml.account_id, aml.date, aml.name as label, am.name, (
                    # aml.debit - aml.credit) as balance, aml.debit, aml.credit, aml.partner_id, aml.user_id as team_member
                    # from account_move_line aml
                    # left join res_users on aml.user_id = res_users.id
                    # join account_move am on
                    # aml.move_id = am.id
                else:
                    print("target_move_else")
                    search_query = "select aml.id, am.id as j_id, aml.account_id, aml.date, " \
                                   "aml.name as label, am.name, " \
                                   + "(aml.debit-aml.credit) as balance, aml.debit, aml.credit, aml.partner_id, aml.user_id as team_member" \
                                   + " from account_move_line aml " \
                                     " join account_move am " \
                                     "on (aml.move_id=am.id) " \
                                   + " where aml.account_id=%s"
                    vals = []
                if form['date_from'] and form['date_to'] and form['team_id']:
                    if form['user_id']:
                        search_query += " and aml.date>=%s and aml.date<=%s and aml.user_id =  %s"
                        vals += [account, form['date_from'], form['date_to'],
                                 form['user_id'][0]]
                    else:
                        search_query += " and aml.date>=%s and aml.date<=%s and aml.user_id = any (%s)"
                        vals += [account, form['date_from'], form['date_to'],
                                 self.env['crm.team'].browse(
                                     form['team_id'][0]).member_ids.mapped(
                                     'id')]
                elif form['date_from'] and form['team_id']:
                    if form['user_id']:
                        search_query += " and aml.date>=%s and aml.user_id =  %s"
                        vals += [account, form['date_from'],form['user_id'][0]]
                    else:
                        search_query += " and aml.date>=%s and aml.user_id = any (%s)"
                        vals += [account, form['date_from'],
                                 self.env['crm.team'].browse(
                                     form['team_id'][0]).member_ids.mapped(
                                     'id')]
                elif form['date_to'] and form['team_id']:
                    if form['user_id']:
                        search_query += " and aml.date<=%s and aml.user_id =  %s"
                        vals += [account, form['date_to'], form['user_id'][0]]
                    else:
                        search_query += " and aml.date<=%s and aml.user_id = any (%s)"
                        vals += [account, form['date_to'],
                                 self.env['crm.team'].browse(
                                     form['team_id'][0]).member_ids.mapped(
                                     'id')]
                elif form['date_from'] and form['date_to']:
                    print("b")
                    search_query += " and aml.date>=%s and aml.date<=%s"
                    vals += [account, form['date_from'], form['date_to']]
                elif form['date_from']:
                    print("c")
                    search_query += " and aml.date>=%s"
                    vals += [account, form['date_from']]
                elif form['date_to']:
                    print("d")
                    search_query += " and aml.date<=%s"
                    vals += [account, form['date_to']]
                elif form['team_id']:
                    if form['user_id']:
                        search_query += " and aml.user_id =  %s"
                        vals += [account, form['user_id'][0]]
                    else:
                        search_query += " and aml.user_id = any (%s)"
                        vals += [account, self.env['crm.team'].browse(
                            form['team_id'][0]).member_ids.mapped('id')]

                else:
                    print("else")
                    vals += [account]
                cr.execute(search_query, tuple(vals))
                items = cr.dictfetchall()
                for j in items:
                    temp = j['id']
                    j['id'] = re.sub('[^0-9a-zA-Z]+', '', i['name']) + str(
                        temp)
                    j['p_id'] = str(i['a_id'])
                    j['type'] = 'journal_item'
                    journal_items.append(j)
        return journal_items

    def _build_contexts(self, data):
        res = super()._build_contexts(data)
        res['user_id'] = data['form']['user_id'] or False
        res['team_id'] = data['form']['team_id'] or False
        return res


class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _query_get(self, domain=None):
        self.check_access_rights('read')

        context = dict(self._context or {})
        domain = domain or []
        if not isinstance(domain, (list, tuple)):
            domain = ast.literal_eval(domain)

        date_field = 'date'
        if context.get('aged_balance'):
            date_field = 'date_maturity'
        if context.get('date_to'):
            domain += [(date_field, '<=', context['date_to'])]
        if context.get('date_from'):
            if not context.get('strict_range'):
                domain += ['|', (date_field, '>=', context['date_from']),
                           ('account_id.user_type_id.include_initial_balance',
                            '=', True)]
            elif context.get('initial_bal'):
                domain += [(date_field, '<', context['date_from'])]
            else:
                domain += [(date_field, '>=', context['date_from'])]
        if context.get('journal_ids'):
            domain += [('journal_id', 'in', context['journal_ids'])]

        state = context.get('state')
        if state and state.lower() != 'all':
            domain += [('parent_state', '=', state)]

        if context.get('company_id'):
            domain += [('company_id', '=', context['company_id'])]
        elif context.get('allowed_company_ids'):
            domain += [('company_id', 'in', self.env.companies.ids)]
        else:
            domain += [('company_id', '=', self.env.company.id)]

        if context.get('reconcile_date'):
            domain += ['|', ('reconciled', '=', False), '|',
                       ('matched_debit_ids.max_date', '>',
                        context['reconcile_date']),
                       ('matched_credit_ids.max_date', '>',
                        context['reconcile_date'])]

        if context.get('account_tag_ids'):
            domain += [
                ('account_id.tag_ids', 'in', context['account_tag_ids'].ids)]

        if context.get('account_ids'):
            domain += [('account_id', 'in', context['account_ids'].ids)]

        if context.get('analytic_tag_ids'):
            domain += [
                ('analytic_tag_ids', 'in', context['analytic_tag_ids'].ids)]

        if context.get('analytic_account_ids'):
            domain += [('analytic_account_id', 'in',
                        context['analytic_account_ids'].ids)]

        if context.get('partner_ids'):
            domain += [('partner_id', 'in', context['partner_ids'].ids)]

        if context.get('partner_categories'):
            domain += [('partner_id.category_id', 'in',
                        context['partner_categories'].ids)]
        if context.get('team_id'):
            if context.get('user_id'):
                domain += [('user_id', '=', context['user_id'][0])]
            else:
                domain += [('user_id', 'in', self.env['crm.team'].browse(
                    context['team_id'][0]).member_ids.mapped('id'))]

        where_clause = ""
        where_clause_params = []
        tables = ''
        if domain:
            domain.append(
                ('display_type', 'not in', ('line_section', 'line_note')))
            domain.append(('parent_state', '!=', 'cancel'))

            query = self._where_calc(domain)

            # Wrap the query with 'company_id IN (...)' to avoid bypassing company access rights.
            self._apply_ir_rules(query)

            tables, where_clause, where_clause_params = query.get_sql()
        return tables, where_clause, where_clause_params

