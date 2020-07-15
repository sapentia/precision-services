# -*- coding: utf-8 -*-

from odoo import models, fields, api

class psg_technical(models.Model):
    _name = 'psg.technical_sys'
    _description = 'System Details'

    name = fields.Char('Technical Reference')
    contract_id = fields.Many2one(
        comodel_name='psg.contract',
        string='Contract',
        required=False)

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=False)

    # General Information

    remote_reset = fields.Selection(
        string='Remote Reset Facility',
        selection=[('y', 'Yes'),
                   ('n', 'No'),],
        required=False, )
    reset_by = fields.Char('Reset By')
    reset_method = fields.Char('Reset Method')
    remote_reset_unit = fields.Many2one(
        comodel_name='product.product',
        string='Remote Reset Unit',
        required=False)

    communicator = fields.Many2one(
        comodel_name='product.product',
        string='Communicator',
        required=False)

    ip_communicator = fields.Many2one(
        comodel_name='product.product',
        string='IP Communicator',
        required=False)

    type_stu = fields.Many2one(
        comodel_name='product.product',
        string='STU Type',
        required=False)

    time_delay = fields.Char('Time Delay')
    cut_out = fields.Char('Cut Out')

    lead_engineer = fields.Many2one(
        comodel_name='res.user',
        string='STU Type',
        required=False)

    panel = fields.Many2one(
        comodel_name='product.product',
        string='Panel (CIE)',
        required=False)

    software_version = fields.Char('Software Version')
    panel_location = fields.Char('Panel Location')
    map_ref = fields.Char('OS Map Ref')
    directions = fields.Text('Directions')
    extent_cover = fields.Text('Extent of Cover')
    cert_description = fields.Text('Description of system covered by certificate')


    #Fire  Equipment Summary

    dep_design = fields.Char('Departure from Design')
    elec_cert = fields.Char('Electrical Certificate')
    des_sched_no = fields.Char('Design Schedule Number')
    drawings = fields.Char('Drawings')
    other_docs = fields.Char('Other Documents')
    op_instruct = fields.Char('Operating Instructions')
    sys_log = fields.Char('System Log Book')
    sys_doc = fields.Char('System Documentation')

    confirm_sys_audio = fields.Selection(
        string='Confirm System Audible',
        selection=[('p', 'Pass'),
                   ('f', 'Fail'),],
        required=False, )

    confirm_sys_visual = fields.Selection(
        string='Confirm System Visual',
        selection=[('p', 'Pass'),
                   ('f', 'Fail'),],
        required=False, )

    confirm_sys_other = fields.Selection(
        string='Confirm System Other',
        selection=[('p', 'Pass'),
                   ('f', 'Fail'),],
        required=False, )

    confirm_wire_audio = fields.Selection(
        string='Confirm System Wired Audible',
        selection=[('p', 'Pass'),
                   ('f', 'Fail'), ],
        required=False, )

    confirm_wire_visual = fields.Selection(
        string='Confirm System Wired Visual',
        selection=[('p', 'Pass'),
                   ('f', 'Fail'), ],
        required=False, )

    confirm_wire_other = fields.Selection(
        string='Confirm System Wired Other',
        selection=[('p', 'Pass'),
                   ('f', 'Fail'), ],
        required=False, )

    sound_lvl = fields.Char('Sound Levels')
    sound_location = fields.Char('Sound at Location')
    further_inspect = fields.Char('Further Inspected')

    sys_new = fields.Boolean('System New')
    sys_add = fields.Boolean('System Additional')
    sys_alt = fields.Boolean('System Alteration')

    false_12 = fields.Integer('False Alarms in 12 Months')
    false_auto = fields.Integer('False Alarms per 100 Auto')


    inst1_model = fields.Char('Instrument 1 (Insulation Resistance) - Model')
    inst1_sno = fields.Char('Instrument 1 (Insulation Resistance)- Serial No')
    inst2_model = fields.Char('Instrument 2 (Continuity) - Model')
    inst2_sno = fields.Char('Instrument 2 (Continuity - Serial No')
    inst3_model = fields.Char('Instrument 3 (Earth fault loop impedance) - Model')
    inst3_sno = fields.Char('Instrument 3 (Earth fault loop impedance) - Serial No')
    inst4_model = fields.Char('Instrument 4 (Sound power level meter) - Model')
    inst4_sno = fields.Char('Instrument 4 (Sound power level meter))- Serial No')
    inst5_model = fields.Char('Instrument 5 (if any) - Model')
    inst5_sno = fields.Char('Instrument 5 (if any - Serial No')
    inst6_model = fields.Char('Instrument 6 (if any) - Model')
    inst6_sno = fields.Char('Instrument 6 (if any) - Serial No')
    comm_sys = fields.Char('Instrument 5 (if any) - Model')
    comm_sys_date = fields.Char('Instrument 5 (if any - Serial No')
    review_by_date = fields.Date('Review Date')
    review_by = fields.Many2one(
        comodel_name='res.user',
        string='Reviewed By',
        required=False)
    variation = fields.Text('Variations from recommendations')