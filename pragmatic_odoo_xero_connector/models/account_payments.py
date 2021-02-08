from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError, Warning
import requests
import json
from odoo import http
import logging
import datetime
import base64
_logger = logging.getLogger(__name__)

class Account_Payment(models.Model):
    _inherit = 'account.payment'

    xero_payment_id = fields.Char(string="Xero Payment Id",copy=False)
    xero_prepayment_id = fields.Char(string="Xero Prepayment Id",copy=False)
    xero_overpayment_id = fields.Char(string="Xero Overpayment Id",copy=False)

    @api.model
    def create_log(self,xero_payment_id,invoice_id):
        xero_config = self.env['res.users'].search([('id', '=', self._uid)], limit=1).company_id
        # print("Payment create function.")

        log_id = self.env['xero.log'].create(
            {
                'company_id': xero_config.id,
                'payment_id': self.id,
                'invoice_id':invoice_id.id,
                'active':True,
                'xero_payment_id': xero_payment_id,
                'payment_status': 'The payment cannot be processed because the invoice is not open!',
            }
        )
        return True

    @api.model
    def delete_log(self,log_search):
        # Deletes the record of the payments from logs when reconciled from front-end
        # print("Payment delete function.")
        log_id = log_search.write(
            {
                'active': False,
            }
        )



    def post(self,xero_payment_id=None,invoice_id=None):
        print("\n POST :-----------------> ",invoice_id, xero_payment_id)
        log_created = None
        AccountMove = self.env['account.move'].with_context(default_type='entry')
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'posted' for inv in rec.invoice_ids):
                # raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))
                if xero_payment_id:
                    log_search = self.env['xero.log'].search([('xero_payment_id', '=', self.xero_payment_id)])
                    if log_search:
                        _logger.info(_("Payment found in Logs details."))
                    elif not log_search:
                        for invoice in invoice_id:
                            if (invoice.state == 'posted'):
                                log_created = self.create_log(xero_payment_id, invoice)
            else:
                log_search = self.env['xero.log'].search([('xero_payment_id', '=', self.xero_payment_id)])
                if log_search:
                    log_created = self.delete_log(log_search)

            # keep the name in case of a payment reset to draft
            # if not rec.name:
            if not log_created:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            moves = AccountMove.create(rec._prepare_payment_moves())
            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()

            # Update the state / move before performing any reconciliation.
            rec.write({'state': 'posted', 'move_name': moves[0].name})


            if rec.payment_type in ('inbound', 'outbound'):

                # ==== 'inbound' / 'outbound' ====
                if rec.invoice_ids:
                    (moves[0] + rec.invoice_ids).line_ids \
                        .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id) \
                        .reconcile()
            elif rec.payment_type == 'transfer':
                # ==== 'transfer' ====
                moves.mapped('line_ids') \
                    .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id) \
                    .reconcile()

        return True

    @api.model
    def _compute_payment_amount(self, invoices, currency, journal, date):
        '''Compute the total amount for the payment wizard.

        :param invoices:    Invoices on which compute the total as an account.invoice recordset.
        :param currency:    The payment's currency as a res.currency record.
        :param journal:     The payment's journal as an account.journal record.
        :param date:        The payment's date as a datetime.date object.
        :return:            The total amount to pay the invoices.
        '''
        company = journal.company_id
        currency = currency or journal.currency_id or company.currency_id
        date = date or fields.Date.today()


        if not invoices:
            return 0.0

        self.env['account.move'].flush(['type', 'currency_id'])
        self.env['account.move.line'].flush(['amount_residual', 'amount_residual_currency', 'move_id', 'account_id'])
        self.env['account.account'].flush(['user_type_id'])
        self.env['account.account.type'].flush(['type'])
        self._cr.execute('''
                SELECT
                    move.type AS type,
                    move.currency_id AS currency_id,
                    SUM(line.amount_residual) AS amount_residual,
                    SUM(line.amount_residual_currency) AS residual_currency
                FROM account_move move
                LEFT JOIN account_move_line line ON line.move_id = move.id
                LEFT JOIN account_account account ON account.id = line.account_id
                LEFT JOIN account_account_type account_type ON account_type.id = account.user_type_id
                WHERE move.id IN %s
                AND account_type.type IN ('receivable', 'payable')
                GROUP BY move.id, move.type
            ''', [tuple(invoices.ids)])
        query_res = self._cr.dictfetchall()

        total = 0.0
        for res in query_res:
            move_currency = self.env['res.currency'].browse(res['currency_id'])
            if move_currency == currency and move_currency != company.currency_id:
                total += res['residual_currency']
                if invoices.xero_invoice_id:
                    if invoices.type == 'out_refund':
                        total=-(invoices.amount_residual)
                    elif invoices.type == 'in_invoice':
                        total = -(invoices.amount_residual)

                    else:
                        total = invoices.amount_residual





            else:
                total += company.currency_id._convert(res['amount_residual'], currency, company, date)
                if invoices.xero_invoice_id:
                    if total == 0.0:
                        if invoices.amount_residual> 0.0:
                            if invoices.type == 'out_refund':
                                total = -(invoices.amount_residual)
                            elif invoices.type == 'in_invoice':
                                total = -(invoices.amount_residual)

                            else:
                                total = invoices.amount_residual
        return total


    def prepare_payment_export_dict(self):
        """Create Dictionary to export to XERO"""
        vals = {}
        # print("\n\n\n\nself :::::::::::::: ",self)
        # print("self.invoice_ids ::::::::::::: ",self.invoice_ids)

        if self.invoice_ids:

            xero_id = False
            if len(self.invoice_ids) == 1:
                for invoice in self.invoice_ids:
                    # if len(self.invoice_ids) == 1:
                    # print("invoice.state : ",invoice.state)
                    # print("invoice.xero_invoice_id ",invoice.xero_invoice_id)
                    if not invoice.xero_invoice_id:
                        if invoice.state == 'open' or invoice.state == 'paid':
                            if (invoice.type == 'out_invoice') or (invoice.type == 'in_invoice'):
                                invoice.exportInvoice(payment_export=True)
                                xero_id = invoice.xero_invoice_id

                            if (invoice.type == 'out_refund') or (invoice.type == 'in_refund'):
                                invoice.exportCreditNote(payment_export=True)
                                xero_id = invoice.xero_invoice_id

                    if invoice.xero_invoice_id:
                        xero_id = invoice.xero_invoice_id
                    if invoice.type == 'out_invoice' or invoice.type == 'in_invoice':
                        ApplyOn = "Invoice"
                        ApplyOn_Dict = {"InvoiceID": xero_id}
                    if invoice.type == 'out_refund' or invoice.type == 'in_refund':
                        ApplyOn = "CreditNote"
                        ApplyOn_Dict = {"CreditNoteID": xero_id}

                    # print"xero_id ::::::::::::: ",xero_id
                    # print"ApplyOn ::::::::::::: ",ApplyOn
                    # print"ApplyOn_Dict ::::::::::::: ",ApplyOn_Dict

                    # print("self.journal_id : ",self.journal_id)
                    # print("self.journal_id.default_debit_account_id : ",self.journal_id.default_debit_account_id)
                    # print("self.journal_id.default_debit_account_id.xero_account_id : ",self.journal_id.default_debit_account_id.xero_account_id)
                    if self.journal_id.default_debit_account_id:
                        if not self.journal_id.default_debit_account_id.xero_account_id:
                            self.env['account.account'].create_account_ref_in_xero(self.journal_id.default_debit_account_id)

                        if xero_id and ApplyOn and ApplyOn_Dict:
                            # if len(self.invoice_ids) > 1:
                            #     vals.update({
                            #         "Payments": [
                            #             {
                            #                 ApplyOn : ApplyOn_Dict,
                            #                 "Account": {"AccountID": self.journal_id.default_debit_account_id.xero_account_id},
                            #                 "Date": self.payment_date,
                            #                 "Amount": self.amount,
                            #                 "Reference": self.name
                            #             }
                            #         ]
                            #     })
                            if len(self.invoice_ids) == 1:
                                vals.update({
                                              ApplyOn: ApplyOn_Dict ,
                                              "Account": {"AccountID": self.journal_id.default_debit_account_id.xero_account_id},
                                              "Date": str(self.payment_date),
                                              "Amount": self.amount,
                                              "Reference": self.name
                                            })
        print('vals :----------------------> ',vals)

        return vals

    # @api.multi
    def get_head(self):
        xero_config = self.env['res.users'].search([('id', '=', self._uid)], limit=1).company_id
        client_id = xero_config.xero_client_id
        client_secret = xero_config.xero_client_secret

        # data = client_id + ":" + client_secret
        data = ('%s:%s' % (client_id, client_secret))
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        encodedStr = str(encodedBytes).encode("utf-8")
        headers = {
            'Authorization': "Bearer " + str(xero_config.xero_oauth_token),
            'Xero-tenant-id': xero_config.xero_tenant_id,
            'Accept': 'application/json'

        }
        return headers


    @api.model
    def create_payment_in_xero(self):
        """export payment to XERO"""
        xero_config = self.env['res.users'].search([('id', '=', self._uid)], limit=1).company_id
        if self._context.get('active_ids'):
            payments = self.browse(self._context.get('active_ids'))
        else:
            payments = self

        for payment in payments:
            if payment.xero_payment_id:
                raise Warning("Payment is already exported to Xero!")
            if not payment.xero_payment_id:
                vals = payment.prepare_payment_export_dict()
                # print("\n vals :",vals)
                if not vals:
                    raise Warning("Payment can not be exported, something went wrong...!!")

                parsed_dict = json.dumps(vals)
                if xero_config.xero_oauth_token:
                    token = xero_config.xero_oauth_token
                headers = self.get_head()
                # print("token : ",token)
                if token:
                    protected_url = 'https://api.xero.com/api.xro/2.0/Payments'
                    data = requests.request('POST', url=protected_url, data=parsed_dict, headers=headers)
                    print("\n\n\nDATA : ", data, data.text)
                    if data.status_code == 200:

                        response_data = json.loads(data.text)
                        if response_data.get('Payments')[0].get('PaymentID'):
                            payment.xero_payment_id = response_data.get('Payments')[0].get('PaymentID')
                            _logger.info(_("(CREATE) - Exported successfully to XERO"))
                    elif data.status_code == 401:
                        raise Warning(
                            "Time Out.\nPlease Check Your Connection or error in application or refresh token..!!")
                    elif data.status_code == 400:
                        logs = self.env['xero.error.log'].create({
                            'transaction': 'Payment Export',
                            'xero_error_response': data.text,
                            'error_date': fields.datetime.now(),
                            'record_id': payment,
                        })
                        self._cr.commit()

                        response_data = json.loads(data.text)
                        if response_data:
                            if response_data.get('Elements'):
                                for element in response_data.get('Elements'):
                                    if element.get('ValidationErrors'):
                                        for err in element.get('ValidationErrors'):
                                            raise Warning(
                                                '(Payment) Xero Exception : ' + err.get(
                                                    'Message'))
                            elif response_data.get('Message'):
                                raise Warning(
                                    '(Payment) Xero Exception : ' + response_data.get(
                                        'Message'))
                            else:
                                raise Warning(
                                    '(Payment) Xero Exception : please check xero logs in odoo for more details')


                else:
                    raise Warning("Please Check Your Connection or error in application or refresh token..!!")

        success_form = self.env.ref('pragmatic_odoo_xero_connector.export_successfull_view', False)
        return {
            'name': _('Notification'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.company.message',
            'views': [(success_form.id, 'form')],
            'view_id': success_form.id,
            'target': 'new',
        }

    @api.model
    def exportPayment_cron(self):
        payment_records = self.env['account.payment'].search([('xero_payment_id', '=', False)])
        for payment in payment_records:
            payment.create_payment_in_xero()