# -*- coding: utf-8 -*-

from odoo import models, fields, api

class psg_contract_type(models.Model):
    _name = 'psg.contract_type'
    _description = 'Contract Type'

    name = fields.Char('Type')
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
    active = fields.Boolean('Active')
    color = fields.Integer('Colour')

class psg_category_grade(models.Model):
    _name = 'psg.category_grade'
    _description = 'Category Grade'

    name = fields.Char('Category Type')
    active = fields.Boolean('Active')
    color = fields.Integer('Colour')

class psg_service_frequency(models.Model):
    _name = 'psg.contract_service_frequency'
    _description = 'Service Frequency'

    name = fields.Char('Frequency')
    active = fields.Boolean('Active')
    color = fields.Integer('Colour')

class psg_invoice_code(models.Model):
    _name = 'psg.invoice_code'
    _description = 'Invoice Code'

    name = fields.Char('Invoice Code')
    active = fields.Boolean('Active')
    color = fields.Integer('Colour')


class psg_paid_by(models.Model):
    _name = 'psg.paid_by'
    _description = 'Paid By'

    name = fields.Char('Payment Method')
    active = fields.Boolean('Active')
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
    active = fields.Boolean('Active')
    color = fields.Integer('Colour')

class psg_loss_reason(models.Model):
    _name = 'psg.loss_reason'
    _description = 'Loss Reasons'

    name = fields.Char('Payment Method')
    active = fields.Boolean('Active')
    color = fields.Integer('Colour')

class psg_contract(models.Model):
    _name = 'psg.contract'
    _description = 'Contracts'

    name = fields.Char('Contract Number')
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=False)
    contact = fields.Many2one(
        comodel_name='res.partner',
        string='Contact',
        required=False)
    job_title = fields.Char('Job Title')
    health_safety = fields.Char('Health & Safety')

    # System Information

    system_type = fields.Many2one(
        comodel_name='psg.systems',
        string='System Type',
        required=False)

    build_standard = fields.Many2one(
        comodel_name='psg.systems',
        string='System Type',
        required=False)

    system_description = fields.Char('System Description')

    primary_signal_type = fields.Char('Primary Signal Type')

    category_type = fields.Many2one(
        comodel_name='psg.category_type',
        string='Category Type',
        required=False)

    grade = fields.Many2one(
        comodel_name='psg.contract_grade',
        string='Grade',
        required=False)

    system_condition = fields.Selection(
        string='System_condition',
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
        string='Contact Type',
        required=False)


    premesis_type = fields.Selection(
        string='Status',
        selection=[('comm', 'Commercial'),
                   ('res', 'Residential'),
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

    warranty_date = fields.Date('Warranty Expires')
    contract_date = fields.Date('Contract Date')
    next_review_date = fields.Date('Next Review Date')
    close_date = fields.Date('Closed Date')

   # PMV Service Setup

    appointment = fields.Selection(
    string='Appointment Required',
    selection=[('y', 'Yes'),
               ('n', 'No'), ],
    required=False, )

    service_frequecy = fields.Many2one(
        comodel_name='psg.contract_service_frequency',
        string='Service Frequency',
        required=False)

    last_service_date = fields.Date('Last Service Date')
    annual_date = fields.Date('Annual Visit Date')
    next_service_date = fields.Date('Next Service Date')

    ann_hours = fields.Float('ANN Service Hours')
    int_hours = fields.Float('INT Service Hours')


    # Remote Monitoring

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

    #  Finance Tab
    maint_from = fields.Date('Maintainance From')
    maint_to = fields.Date('Maintainance To')
    account_number = fields.Char('Account Number')
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
    email_invoice = fields.Boolean('Email Invoice?')
    po_req_callout = fields.Boolean('PO Required - Call Out?')
    callout_po = fields.Char('Call Out PO Number')
    callout_po_expires = fields.Char('Call Out Expires')
    po_req_main = fields.Boolean('PO Required - Maintenance?')
    maint_po = fields.Char('Maint PO Number')
    maint_po_expires = fields.Char('Maint Expires')

    urn_ids  = fields.One2many(
        comodel_name='psg.urns',
        inverse_name='contract_id',
        string='URNs',
        required=False)

    private_notes = fields.Text('Private Notes')
    notes = fields.Text('Notes')

    engineer_notes = fields.Text('Engineer Notes')
    service_reminder_1 = fields.Char('Service Reminder 1')
    service_reminder_2 = fields.Char('Service Reminder 2')
    service_reminder_3 = fields.Char('Service Reminder 3')
    service_reminder_4 = fields.Char('Service Reminder 4')

    service_reminder_date_1 = fields.Date('Service Reminder Date 1')
    service_reminder_date_2 = fields.Date('Service Reminder Date 2')
    service_reminder_date_3 = fields.Date('Service Reminder Date 3')
    service_reminder_date_4 = fields.Date('Service Reminder Date4')

   #  Loss Details

    loss_date = fields.Date('Loss Date')
    loss_effective_date = fields.Date('Loss Effective Date')
    loss_reason = fields.Many2one(
        comodel_name='psg.loss_reason',
        string='Loss Reason',
        required=False)
    details_removed = fields.Date('Details Removed')
    lost_serivce_pa = fields.Char('Lost Service PA')
    destroy_docs = fields.Selection(
        string='Destroy Documents',
        selection=[('y', 'Yes'),
                   ('n', 'No'), ],
        required=False, )
