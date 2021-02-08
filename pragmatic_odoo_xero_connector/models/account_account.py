import base64

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError, Warning
import requests
import json
from odoo import http
import logging
import datetime
_logger = logging.getLogger(__name__)

class Account(models.Model):
    _inherit = 'account.account'

    xero_account_id = fields.Char(string="Xero Account Id",copy=False)
    enable_payments_to_account = fields.Boolean(string="Enable Payments",default=False,copy=False)
    xero_account_type = fields.Many2one('xero.account.account',string="Xero Account Type")
    xero_description = fields.Text(string="Description")
    xero_tax_type_for_accounts = fields.Many2one('xero.tax.type',string="Tax Type")

    @api.model
    def prepare_account_export_dict(self):
        """Create Dictionary to export to XERO"""
        vals = {}
        if self.code:
            vals.update({
                'Code': self.code,
                'TaxType':'NONE'
            })
        if self.name:
            vals.update({
                'Name': self.name,
            })
        if self.enable_payments_to_account:
            if self.enable_payments_to_account == True:
                vals.update({
                    'EnablePaymentsToAccount': 'true',
                })
            else:
                vals.update({
                    'EnablePaymentsToAccount': 'false',
                })
        if self.xero_description:
            vals.update({
                'Description': self.xero_description,
            })
        if self.xero_tax_type_for_accounts:
            vals.update({
                'TaxType': self.xero_tax_type_for_accounts.xero_tax_type,
            })
        if self.xero_account_type:
            account_type = {'Current Asset account': 'CURRENT',
                            'Current Liability account':'CURRLIAB',
                            'Depreciation account':'DEPRECIATN' ,
                            'Direct Costs account':'DIRECTCOSTS',
                            'Equity account':'EQUITY',
                            'Expense account':'EXPENSE',
                            'Fixed Asset account':'FIXED' ,
                            'Inventory Asset account': 'INVENTORY',
                            'Liability account':'LIABILITY',
                            'Non-current Asset account':'NONCURRENT',
                            'Other Income account':'OTHERINCOME',
                            'Overhead account':'OVERHEADS',
                            'Prepayment account':'PREPAYMENT',
                            'Revenue account':'REVENUE',
                            'Sale account':'SALES',
                            'Non-current Liability account':'TERMLIAB',
                            }

            type_name =  self.env['xero.account.account'].search([('id','=',self.xero_account_type.id)])
            if type_name.xero_account_type_name in account_type:
                vals.update({
                        'Type': account_type.get(type_name.xero_account_type_name)
                })
        return vals

    @api.model
    def create_account_in_xero(self):
        """export accounts to XERO"""

        xero_config = self.env['res.users'].search([('id', '=', self._uid)], limit=1).company_id
        if self._context.get('active_ids'):
            account = self.browse(self._context.get('active_ids'))
        else:
            account = self

        for a in account:
            self.create_account_main(a, xero_config)
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
    def create_account_ref_in_xero(self,account_id):
        """export accounts to XERO"""
        xero_config = self.env['res.users'].search([('id', '=', self._uid)], limit=1).company_id
        # if self._context.get('active_ids'):
        #     account = self.browse(self._context.get('active_ids'))
        # else:
        if account_id:
            account = account_id
        else:
            account = self
        if account:
            self.create_account_main(account, xero_config)

    def get_head(self):

        xero_config = self.env['res.users'].search([('id', '=', self._uid)], limit=1).company_id
        client_id = xero_config.xero_client_id
        client_secret = xero_config.xero_client_secret

        data = client_id + ":" + client_secret
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        headers = {
            'Authorization': "Bearer " + str(xero_config.xero_oauth_token),
            'Xero-tenant-id': xero_config.xero_tenant_id,
            'Accept': 'application/json'

        }
        return headers




    @api.model
    def create_account_main(self,a,xero_config):
            if not a.xero_account_type:
                # abc = acc.code
                raise Warning('Please Add Xero Account Type and Tax Type for Account No ' + a.code)
            else:
                if not a.xero_account_id:
                    vals = a.prepare_account_export_dict()
                    parsed_dict = json.dumps(vals)
                    # print("PARSED DICT : ",parsed_dict,type(parsed_dict))

                    if xero_config.xero_oauth_token:
                        token = xero_config.xero_oauth_token

                    headers = self.get_head()
                    if token:
                        client_key = xero_config.xero_client_id
                        client_secret = xero_config.xero_client_secret
                        resource_owner_key = xero_config.xero_oauth_token
                        resource_owner_secret = xero_config.xero_oauth_token_secret

                        protected_url = 'https://api.xero.com/api.xro/2.0/Accounts'
                        data = requests.request('PUT',url=protected_url,data=parsed_dict,headers=headers)
                        # print("DATA : ",data,data.text)
                        if data.status_code == 200:
                            response_data = json.loads(data.text)
                            if response_data.get('Accounts'):
                                # update xero accound id
                                if response_data.get('Accounts')[0].get('AccountID'):
                                    a.update({
                                       'xero_account_id' :  response_data.get('Accounts')[0].get('AccountID')
                                    })
                                    self._cr.commit()
                                    # print("ACC ID : ",a.xero_account_id)
                                    _logger.info(_(" (CREATE) - Exported successfully to XERO"))
                                    # self._cr.commit()
                                        # self.SuccessMessage()
                        elif data.status_code == 400:
                            logs = self.env['xero.error.log'].create({
                                'transaction': 'Account Export',
                                'xero_error_response': data.text,
                                'error_date': fields.datetime.now(),
                                'record_id': a,
                            })
                            self._cr.commit()
                            response_data = json.loads(data.text)
                            if response_data:
                                if response_data.get('Elements'):
                                    for element in response_data.get('Elements'):
                                        if element.get('ValidationErrors'):
                                            for err in element.get('ValidationErrors'):
                                                if err.get('Message'):
                                                    raise Warning('(Account) Xero Exception : ' + err.get('Message'))
                                elif response_data.get('Message'):
                                    raise Warning(
                                        '(Account) Xero Exception : ' + response_data.get('Message'))
                                else:
                                    raise Warning(
                                        '(Account) Xero Exception : please check xero logs in odoo for more details')
                        elif data.status_code == 401:
                            raise Warning("Time Out.\nPlease Check Your Connection or error in application or refresh token..!!")

                elif a.xero_account_id:
                    vals = a.prepare_account_export_dict()
                    parsed_dict = json.dumps(vals)
                    if xero_config.xero_oauth_token:
                        token = xero_config.xero_oauth_token

                    headers=self.get_head()
                    if token:
                        client_key = xero_config.xero_client_id
                        client_secret = xero_config.xero_client_secret
                        resource_owner_key = xero_config.xero_oauth_token
                        resource_owner_secret = xero_config.xero_oauth_token_secret

                        protected_url = 'https://api.xero.com/api.xro/2.0/Accounts/'+a.xero_account_id

                        data = requests.request('POST', url=protected_url, headers=headers, data=parsed_dict)
                        # print("DATA ----------------> ", data, data.text)
                        if data.status_code == 200:
                            _logger.info(_(" (UPDATE) - Exported successfully to XERO"))
                        elif data.status_code == 401:
                            raise Warning("Time Out..!!\nPlease Check Your Connection or error in application or refresh token.")
                        else:
                            logs = self.env['xero.error.log'].create({
                                'transaction': 'Account Export',
                                'xero_error_response': data.text,
                                'error_date': fields.datetime.now(),
                                'record_id': a,
                            })
                            self._cr.commit()

class XeroAccountType(models.Model):
    _name = 'xero.account.account'
    _description = 'xero account account'
    _rec_name = 'xero_account_type_name'

    xero_account_type_name = fields.Char(string='Account Type', readonly=True,copy=False)

class XeroAccountTaxType(models.Model):
    _name = 'xero.tax.type'
    _description = 'xero tax type'
    _rec_name = 'xero_tax_type'

    xero_tax_type = fields.Char(string='Account Tax Type', readonly=True,copy=False)

