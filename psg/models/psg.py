# -*- coding: utf-8 -*-

from odoo import models, fields, api


class psg_systems(models.Model):
    _name = 'psg.systems'
    _description = 'Systems'

    name = fields.Char('System Type')
    code = fields.Char('Code')
    description = fields.Text('Friendly Name')
    curr_build_std = fields.Char('Current Build Standard')
    cert_code = fields.Char('Certification Code')
    cert_layout = fields.Char('Certification Code')
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
    street2 = fields.Char('Address 1')
    city = fields.Char('Address 1')
    county = fields.Char('Address 1')
    postcode = fields.Char('Address 1')


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
    street2 = fields.Char('Address 1')
    city = fields.Char('Address 1')
    county = fields.Char('Address 1')
    postcode = fields.Char('Address 1')

