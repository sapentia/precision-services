# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class psg_contract_type(models.Model):
    _name = 'psg.contract_type'
    _description = 'Contract Type'

    name = fields.Char('Type')
    active = fields.Boolean('Active',default=True)
    charge_type = fields.Char('Charge Type')
    call_out1 = fields.Float('Call Out 1')
    call_out2 = fields.Float('Call Out 2')
    labour_1a = fields.Float('Labour 1A')
    labour_1b = fields.Float('Labour 1b')
    labour_2a = fields.Float('Labour 2A')
    labour_2b = fields.Float('Labour 2b')



class psg_category_type(models.Model):
    _name = 'psg.category_type'
    _description = 'Category Type'

    name = fields.Char('Category Type')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')

class psg_category_grade(models.Model):
    _name = 'psg.category_grade'
    _description = 'Category Grade'

    name = fields.Char('Category Type')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')

class psg_service_frequency(models.Model):
    _name = 'psg.contract_service_frequency'
    _description = 'Service Frequency'

    name = fields.Char('Frequency')
    interval_days = fields.Float('Days between Visits')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')

class psg_invoice_code(models.Model):
    _name = 'psg.invoice_code'
    _description = 'Invoice Code'

    name = fields.Char('Invoice Code')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')

class psg_health_safety(models.Model):
    _name = 'psg.health_safety'
    _description = 'Health & Safety'

    name = fields.Char('Name')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')


class psg_paid_by(models.Model):
    _name = 'psg.paid_by'
    _description = 'Paid By'

    name = fields.Char('Payment Method')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')


class psg_urns(models.Model):
    _name = 'psg.urns'
    _description = 'URNs'

    name = fields.Char('URN Ref')
    response = fields.Char('Response')
    withdrawn_from = fields.Date('Withdrawn From')
    remind = fields.Date('Remind')
    up_to = fields.Date('Up To')
    detect_no = fields.Integer('No Detectors')
    no_level_1 = fields.Integer('Level 1 Incidents')
    level_1 = fields.Char('Level 1 Months')
    no_level_2 = fields.Integer('Level 2 Incidents')
    level_2 = fields.Char('Level 2 Months')
    contract_id  = fields.Many2one(
        comodel_name='psg.contract',
        string='Contract',
        required=False)
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')


class psg_remote(models.Model):
    _name = 'psg.remote'
    _description = 'Remote Monitoring'

    name = fields.Char('Remote Monitoring Ref')
    remote_signal = fields.Selection(
        string='Remote Signal',
        selection=[('y', 'Yes'),
                   ('n', 'No'), ],
        required=False, )

    cd_digi = fields.Char('CS Digi No')
    stu = fields.Char('STU No')
    remote_ip = fields.Char('Remote IP')
    central = fields.Char('Central Station', default='EMCS Ltd')
    fire_authority = fields.Many2one(
        comodel_name='psg.fire_service',
        string='Fire Authority',
        required=False)

    police_authority = fields.Many2one(
        comodel_name='psg.police_service',
        string='Police Authority',
        required=False)

    verification = fields.Selection(
        string='Verification Method',
        selection=[('none', 'None'),
                   ('audio', 'Audio'),
                   ('video', 'Video'),
                   ('point', 'Point ID'),
                   ('seq', 'Sequential'), ],
        required=False, )
    contract_id  = fields.Many2one(
        comodel_name='psg.contract',
        string='Site',
        required=False)
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')


class psg_pmv(models.Model):
    _name = 'psg.pmv'
    _description = 'PMVs'

    name = fields.Char('PMV Ref')
    appointment = fields.Selection(
        string='Appointment Required',
        selection=[('y', 'Yes'),
                   ('n', 'No'), ],
        required=False, )

    service_frequency = fields.Many2one(
        comodel_name='psg.contract_service_frequency',
        string='Service Frequency',
        required=False)

    # @api.model
    # @api.depends('last_service_date','service_frequency')
    # def _get_next_service(self):
    #     if self.last_service_date:
    #         for record in self:
    #             days = record.service_frequency.interval_days or 0
    #             if days > 0:
    #                 record.next_service_date = fields.Date.to_string(record.last_servive_date + timedelta(days))

    last_service_date = fields.Date('Last Service Date')
    first_visit_due = fields.Date('First Visit Due')
    annual_date = fields.Date('Annual Visit Date')
    next_service_date = fields.Date('Next Service Date')

    ann_hours = fields.Float('ANN Service Hours')
    int_hours = fields.Float('INT Service Hours')

    contract_id  = fields.Many2one(
        comodel_name='psg.contract',
        string='Site',
        required=False)
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')


class psg_loss_reason(models.Model):
    _name = 'psg.loss_reason'
    _description = 'Loss Reasons'

    name = fields.Char('Payment Method')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')


class psg_site_spec(models.Model):
    _name = 'psg.site_spec'
    _description = 'Site Specification Types'

    name = fields.Char('Site Specification')
    title = fields.Text('Title Block')
    title_active = fields.Boolean('Title Active', default=True)
    opening_block = fields.Text('Opening Block')
    open_active = fields.Boolean('Opening Active', default=True)
    mid_block = fields.Text('Mid Text Block')
    mid_active = fields.Boolean('Mid Active', default=True)
    closing_block = fields.Text('Closing Block')
    closing_active = fields.Boolean('Closing Active', default=True)
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Colour')



class psg_contract(models.Model):
    _name = 'psg.contract'
    _inherit = ['mail.thread']
    _description = 'Sites'

    name = fields.Char('Site Number')
    active = fields.Boolean('Active', default=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=False)
    contact = fields.Many2one(
        comodel_name='res.partner',
        string='Contact',
        required=False)
    account_number = fields.Char('Account Number')
    job_title = fields.Char('Job Title')
    health_safety  = fields.Many2many(
        comodel_name='psg.health_safety',
        string='Health and Safety')

    # System Information

    system_type = fields.Many2one(
        comodel_name='psg.systems',
        string='System Type',
        required=False)

    build_standard = fields.Many2one(
        comodel_name='psg.build_standard',
        string='Build Standard',
        required=False)

    system_description = fields.Char('System Description')

    primary_signal_type = fields.Char('Primary Signal Type')

    technical_sys = fields.Many2one(
        comodel_name='psg.technical_sys',
        string='Technical Specification',
        required=False)

    category_type = fields.Many2one(
        comodel_name='psg.category_type',
        string='Category Type',
        required=False)

    grade = fields.Many2one(
        comodel_name='psg.category_grade',
        string='Grade',
        required=False)

    system_condition = fields.Selection(
        string='System Condition',
        selection=[('green', 'Green'),
                   ('amber', 'Amber'),
                   ('red', 'Red'),],
        required=False, )

    status = fields.Selection(
        string='Status',
        selection=[('live', 'Live'),
                   ('dead', 'Dead'),],
        required=False, )

    contract_type = fields.Many2one(
        comodel_name='psg.contract_type',
        string='Contract Type',
        required=False)


    premesis_type = fields.Selection(
        string='Premesis Type',
        selection=[('comm', 'Commercial'),
                   ('res', 'Residential'),
                   ('ind', 'Industrial'),
                   ('man', 'Manufacturing'),
                   ('land', 'Landlord Owned'),
                   ('pub', 'Public Sector'),
                   ('retail', 'Retail'),],
        required=False, )

    #Site Details

    site_address = fields.Many2one(
        comodel_name='res.partner',
        string='Site Address',
        required=False)
    site_email = fields.Char('Email')
    site_mobile = fields.Char('Mobile')
    site_phone = fields.Char('Phone')


    # Date Information

    install_date = fields.Date('Installation Date')
    contract_start = fields.Date('Contract Start Date')
    specification_date = fields.Date('Specification')
    warranty_date = fields.Date('Warranty Expires')
    contract_expire_date = fields.Date('Contract Expires Date')
    next_review_date = fields.Date('Contract Review Date')
    close_date = fields.Date('Contract Closed Date')

   # PMV Service Setup ids

    pmv_ids = fields.One2many(
        comodel_name='psg.pmv',
        inverse_name='contract_id',
        string='PMVs',
        required=False)

    appointment = fields.Selection(
        string='Appointment Required',
        selection=[('y', 'Yes'),
                   ('n', 'No'), ],
        required=False, )

    service_frequency = fields.Many2one(
        comodel_name='psg.contract_service_frequency',
        string='Service Frequency',
        required=False)

    last_service_date = fields.Date('Last Service Date')
    first_visit_due = fields.Date('First Visit Due')
    annual_date = fields.Date('Annual Visit Date')
    next_service_date = fields.Date('Next Service Date')
    ann_hours = fields.Float('ANN Service Hours')
    int_hours = fields.Float('INT Service Hours')

    # System Types
    fire_ids = fields.One2many(
        comodel_name='psg.fa_asset',
        inverse_name='contract_id',
        string='Fire Assets',
        required=False)

    ext_ids = fields.One2many(
        comodel_name='psg.ext_asset',
        inverse_name='contract_id',
        string='Extinguiser Assets',
        required=False)


    eml_ids = fields.One2many(
        comodel_name='psg.eml_asset',
        inverse_name='contract_id',
        string='Emergency Lighting Assets',
        required=False)

    # Misc
    rel_quote = fields.Many2one(
        comodel_name='sale.order',
        string='Related Quote/Sale Order',
        required=False)

    rel_contract = fields.Many2one(
        comodel_name='psg.contract',
        string='Related Contract',
        required=False)

    # Remote Monitoring



    remote_ids = fields.One2many(
        comodel_name='psg.remote',
        inverse_name='contract_id',
        string='Remote Monitoring',
        required=False)



    #  Finance Tab
    maint_from = fields.Date('Maintainance From')
    maint_to = fields.Date('Maintainance To')
    call_account_number = fields.Char('Call Out Account Number')
    call_out_account = fields.Char('Call Out Account')
    inv_code = fields.Many2one(
        comodel_name='psg.invoice_code',
        string='Invoice Code',
        required=False)
    paid_by = fields.Many2one(
        comodel_name='psg.paid_by',
        string='Paid By',
        required=False)

    maint_rate = fields.Float('Maintenance Charge')
    mon_rate = fields.Float('Monitoring Charge')
    key_rate = fields.Float('Key Holding Charge')
    guard_rate = fields.Float('Guard Charge')
    call_out_includes = fields.Float('Call Out Includes')
    travel_time = fields.Float('Travel Time (hrs)')
    email_invoice = fields.Selection(string='Verification Method',
                        selection=[('email', 'Email'),
                                   ('post', 'Post Invoice'),
                                   ('print', 'Print Invoice'), ],
                            required=False, default='email' )
    po_req_callout = fields.Boolean('PO Required - Call Out?')
    callout_po = fields.Char('Call Out PO Number')
    callout_po_expires = fields.Date('Call Out Expires')
    po_req_main = fields.Boolean('PO Required - Maintenance?')
    maint_po = fields.Char('Maint PO Number')
    maint_po_expires = fields.Date('Maint Expires')

    urn_ids  = fields.One2many(
        comodel_name='psg.urns',
        inverse_name='contract_id',
        string='URNs',
        required=False)

    private_notes = fields.Text('Private Notes',track_visibility='onchange')
    notes = fields.Text('Notes',track_visibility='onchange')

    engineer_notes = fields.Text('Engineer Notes',track_visibility='onchange')
    copy_notes_single = fields.Boolean('Copy Single Site')
    copy_notes_multi = fields.Boolean('Copy Multiple Sites')
    service_reminder_1 = fields.Char('Service Reminder 1')
    service_reminder_2 = fields.Char('Service Reminder 2')
    service_reminder_3 = fields.Char('Service Reminder 3')
    service_reminder_4 = fields.Char('Service Reminder 4')

    service_reminder_date_1 = fields.Date('Service Date 1')
    service_reminder_date_2 = fields.Date('Service Date 2')
    service_reminder_date_3 = fields.Date('Service Date 3')
    service_reminder_date_4 = fields.Date('Service Date 4')

   #  Loss Details

    loss_date = fields.Date('Loss Date')
    loss_effective_date = fields.Date('Loss Effective Date')
    loss_reason = fields.Many2one(
        comodel_name='psg.loss_reason',
        string='Reason for Loss',
        required=False, track_visibility='onchange')
    details_removed = fields.Date('Details Removed')
    lost_serivce_pa = fields.Char('Lost Service PA')
    destroy_docs = fields.Selection(
        string='Destroy Documents',
        selection=[('y', 'Yes'),
                   ('n', 'No'), ],
        required=False, )

