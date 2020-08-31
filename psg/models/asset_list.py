# -*- coding: utf-8 -*-

from odoo import models, fields, api


class psg_asset_list(models.Model):
    _name = 'psg.asset_list'
    _description = 'Asset Lists'
    _inherit = ['mail.thread']

    name = fields.Char('Name')
    site  = fields.Many2one(
        comodel_name='psg.contract',
        string='Site',
        required=False)
    active = fields.Boolean('Active', default=True)
    list_type  = fields.Selection(
        string='List Type',
        selection=[('eml', 'Emergency Lighting'),
                   ('ext', 'Fire Extinguiser'),
                   ('fa', 'Fire Alarm'),
                   ('phc', 'Pump House Checklist'),
                   ('phc', 'Sprinkler Weekly Checklist'),],
        required=False, )
    panel = fields.Char('Panel/Make/Model/Type')
    panel_location = fields.Char('Panel Location')
    system_category = fields.Char('System Category')
    date = fields.Date('Date')
    eml_asset_ids  = fields.One2many(
        comodel_name='psg.eml_asset',
        inverse_name='list_id',
        string='Emergency Lighting Assets',
        required=False)

    ext_asset_ids  = fields.One2many(
        comodel_name='psg.ext_asset',
        inverse_name='list_id',
        string='Emergency Lighting Assets',
        required=False)

    fa_asset_ids  = fields.One2many(
        comodel_name='psg.fa_asset',
        inverse_name='list_id',
        string='Emergency Lighting Assets',
        required=False)

    pump_check_ids  = fields.One2many(
        comodel_name='psg.pump_check',
        inverse_name='list_id',
        string='Emergency Lighting Assets',
        required=False)

    sprinkler_weekly_ids = fields.One2many(
        comodel_name='psg.sprinkler_weekly',
        inverse_name='list_id',
        string='Emergency Lighting Assets',
        required=False)


class psg_eml_asset(models.Model):
    _name = 'psg.eml_asset'
    _description = 'Emergency Lighting Asset'
    _inherit = ['mail.thread']

    active = fields.Boolean('Active', default=True)
    seq = fields.Integer('Sequence')
    name = fields.Char('Fitting No')
    fitting_location = fields.Char('Fitting Location')
    fitting_type = fields.Char('Fitting Type')
    inspection_comments = fields.Char('Inspection Comments')
    duration = fields.Boolean('Duration Pass')
    neon = fields.Boolean('Neon Pass')
    charging_light = fields.Boolean('Charging Light Pass')
    test_date = fields.Date('Test Date')
    list_id = fields.Many2one(
        comodel_name='psg.asset_list',
        string='Asset List',
        required=False)

    contract_id = fields.Many2one(
        comodel_name='psg.contract',
        string='Site',
        required=False)

class psg_ext_asset(models.Model):
    _name = 'psg.ext_asset'
    _description = 'Fire Extinguisher Asset'
    _inherit = ['mail.thread']

    active = fields.Boolean('Active', default=True)
    seq = fields.Integer('Sequence')
    name = fields.Char('Unit No')
    fitting_location = fields.Char('Extinguiser Location')
    fitting_type = fields.Char('Extinguiser Type')
    inspection_comments = fields.Char('Inspection Comments')
    install_date = fields.Date('Install Date')
    test_date = fields.Date('DTR Due Date')
    list_id = fields.Many2one(
        comodel_name='psg.asset_list',
        string='Asset List',
        required=False)

    contract_id = fields.Many2one(
        comodel_name='psg.contract',
        string='Site',
        required=False)

class psg_fa_asset(models.Model):
    _name = 'psg.fa_asset'
    _description = 'Fire Alarm Asset'
    _inherit = ['mail.thread']

    active = fields.Boolean('Active', default=True)
    seq = fields.Integer('Sequence')
    name = fields.Char('Panel No')
    loop_no = fields.Char('Loop No')
    zone_no = fields.Char('Zone No')
    device_no = fields.Char('Device No')
    device_type = fields.Char('Device Type')
    location = fields.Char('Device Location')
    q1_date = fields.Date('Q1 Maintenance Date')
    q2_date = fields.Date('Q2 Maintenance Date')
    q3_date = fields.Date('Q3 Maintenance Date')
    q4_date = fields.Date('Q4 Maintenance Date')
    list_id = fields.Many2one(
        comodel_name='psg.asset_list',
        string='Asset List',
        required=False)
    contract_id = fields.Many2one(
        comodel_name='psg.contract',
        string='Site',
        required=False)

class psg_pump_check(models.Model):
    _name = 'psg.pump_check'
    _description = 'Pump House Checklist'
    _inherit = ['mail.thread']

    active = fields.Boolean('Active', default=True)
    seq = fields.Integer('Sequence')
    name = fields.Char('Site')
    week_date = fields.Date('Week Ending')
    temp_min = fields.Float('Min Temp')
    temp_before = fields.Float('Temp Before')
    temp_after = fields.Float('Temp After')
    cut_in_press_jp = fields.Char('Cut In Pressure')
    lamp_check = fields.Boolean('Lamp Check')
    cut_in_press_elec = fields.Char('Cut In Pressure')
    churning_press_elec = fields.Char('Churning Pressure')
    churning_current_elec = fields.Char('Churning Current')
    oil_level_dsl = fields.Boolean('Engine Oil Level Checked')
    batt_charger_dsl = fields.Boolean('Batteries and Charger in Order')
    cut_in_press_dsl = fields.Char('Cut In Pressure')
    cool_circ_dsl = fields.Boolean('Coolant Circulating')
    engine_speed_dsl = fields.Char('Engine Speed')
    churning_press_dsl = fields.Char('Churning Pressure')
    engine_oil_press_dsl = fields.Char('Engine Oil Pressure')
    engine_oil_temp_dsl = fields.Char('Engine Oil Temp')
    manual_start_dsl = fields.Boolean('Manual Start in Order')
    run_time_dsl = fields.Char('Time Engine Run (mins)')
    total_hrs_dsl = fields.Char('Total Hours Run')
    fuel_topped_dsl = fields.Boolean('Fuel Tank Topped Up')
    return_normal_dsl = fields.Boolean('All Values to Normal')
    alarm_reset = fields.Boolean('Alarm Reset and Signaling online')
    tester = fields.Many2one(
        comodel_name='res.users',
        string='Tested By',
        required=False)
    list_id = fields.Many2one(
        comodel_name='psg.asset_list',
        string='Asset List',
        required=False)


class psg_sprinkler_weekly(models.Model):
    _name = 'psg.sprinkler_weekly'
    _description = 'Sprinkler Weekly Tests'
    _inherit = ['mail.thread']

    active = fields.Boolean('Active', default=True)
    seq = fields.Integer('Sequence')
    name = fields.Date('Date')
    valve_exercised = fields.Boolean('Valves Exercised')
    alarm_sound = fields.Boolean('Gong / Alarm Sounds')
    alarm_op = fields.Boolean('Fire Alarm Operated')
    comments = fields.Char('Concerns or actions required')
    signature = fields.Binary('Signature')
    list_id = fields.Many2one(
        comodel_name='psg.asset_list',
        string='Asset List',
        required=False)
