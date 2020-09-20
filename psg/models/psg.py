# -*- coding: utf-8 -*-

from odoo import models, fields, api

class psg_build_standard(models.Model):
    _name = 'psg.build_standard'
    _description = 'Build Standards'

    name = fields.Char('Build Standards')
    code = fields.Char('Code')
    description = fields.Text('Friendly Name')


class psg_systems(models.Model):
    _name = 'psg.systems'
    _description = 'Systems'

    name = fields.Char('System Type')
    code = fields.Char('Code')
    description = fields.Text('Friendly Name')
    curr_build_std  = fields.Many2one(
        comodel_name='psg.build_standard',
        string='Current Build Standard',
        required=False)
    cert_code = fields.Char('Certification Code')
    cert_layout = fields.Char('Certification Layout')
    ann_insp = fields.Char('Annual Inspection')
    call_insp = fields.Char('Call Out Inspection')
    install_sheet = fields.Char('Installation')
    group_code = fields.Char('Group Code')

class psg_fire_service(models.Model):
    _name = 'psg.fire_service'
    _description = 'Fire Brigades'

    name = fields.Char('Brigade')
    auth_code = fields.Char('Authority Code')
    street = fields.Char('Address 1')
    street2 = fields.Char('Address 2')
    city = fields.Char('City')
    county = fields.Char('County')
    postcode = fields.Char('Postcode')


class psg_police_service(models.Model):
    _name = 'psg.police_service'
    _description = 'Police Service'

    name = fields.Char('Police Authority')
    area_code = fields.Char('Area Code')
    verified = fields.Boolean('Verified')
    contact = fields.Char('Contact')
    position = fields.Char('Position')
    level1_incidents = fields.Integer('Level 1 Incidents')
    level1_months = fields.Integer('Level 1 Months')
    level2_incidents = fields.Integer('Level 2 Incidents')
    level2_months = fields.Integer('Level 2 Months')
    street = fields.Char('Address 1')
    street2 = fields.Char('Address 2')
    city = fields.Char('City')
    county = fields.Char('County')
    postcode = fields.Char('Postcode')


class psg_psu(models.Model):
    _name = 'psg.psu'
    _description = 'Power Supply Unit Checks'

    name = fields.Char('PSU Number')
    psu_spur = fields.Boolean('Are all PSUs Connected to Spur')
    psu_ln = fields.Float('Mains voltage Live to Neutral (roughly 240AC)')
    psu_le = fields.Float('Mains voltage Live to Earth (roughly 240AC)')
    psu_ne = fields.Float('Mains voltage Neutral to Earth (roughly 240AC)')
    psu_aux = fields.Float('Auxillary Output Voltage')
    psu_bat = fields.Float('Battery charge Voltage (roughly 13vDC)')
    psu_elec_battery = fields.Boolean('Electronic battery test - is the battery ok')

class psg_cu(models.Model):
    _name = 'psg.cu'
    _description = 'Control Unit Checks'

    name = fields.Char('Door Number')
    cu_locks = fields.Float('Output voltage to lock')
    cu_lop = fields.Boolean('Lock operates correctly?')
    cu_reader = fields.Float('Output voltage to reader/keypad')
    cu_kop = fields.Boolean('Keypad operates correctly?')
    cu_exit = fields.Boolean('Exit buttons and Break Glass operate correctly')


class psg_cu_psu(models.Model):
    _name = 'psg.cu_psu'
    _description = 'Power Supply and Control Unit Checks'

    name = fields.Char('Panel Number')
    cpsu_spur = fields.Boolean('Are all PSUs Connected to Spur')
    cpsu_three_amp = fields.Boolean('Is the Panel/PSU connected to 3 Amp spur')
    cpsu_ln = fields.Float('Mains voltage Live to Neutral (roughly 240AC)')
    cpsu_le = fields.Float('Mains voltage Live to Earth (roughly 240AC)')
    cpsu_ne = fields.Float('Mains voltage Neutral to Earth (roughly 240AC)')
    cpsu_trans = fields.Float('Transformer Voltage')
    cpsu_loop = fields.Float('Zone/Loop output Voltage')
    cpsu_bat_test = fields.Char('Electronic battery test(Voltage/Ah and "R" if replaced')
    cpsu_bat = fields.Float('Battery charge Voltage')
    cpsu_qui = fields.Char('Quiescent current(I1)/Alarm current(I2)')
    cpsu_elec_battery = fields.Boolean('Electronic battery test - is the battery ok')
    cpsu_batt_calc = fields.Char('Batteries suitable for installation (Record results 1.25x((Standby Time x I1) + 1.75 x (0.5 x I2))')
    cpsu_batt_replace = fields.Boolean('Replace batteries in wireless devices if required')