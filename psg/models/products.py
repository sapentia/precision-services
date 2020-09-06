# -*- coding: utf-8 -*-

from odoo import models, fields, api


class psg_products(models.Model):
    _inherit = 'product.template'

    sec_grade = fields.Integer('Security Grade')
    env_class = fields.Char('Environmental Class')
    applies_to_ids = fields.Char('Applies to')
    install = fields.Float('Installation Hours')
    amps = fields.Float('Amp Rating')
    manufacturer  = fields.Char('Manufacturer')
    model_no = fields.Char('Model Number')




class psg_applications(models.Model):
    _name = 'psg.application'
    _description = 'Application'

    name = fields.Char('Application')
    active = fields.Boolean('Active', default=True)
    product_id = fields.Char('Product')


class psg_(models.Model):
    _inherit = 'res.partner'


    contract_ids = fields.One2many(
        comodel_name='psg.contract',
        inverse_name='partner_id',
        string='Sites',
        required=False)

    technical_ids = fields.One2many(
        comodel_name='psg.technical_sys',
        inverse_name='partner_id',
        string='Technical Systems Data',
        required=False)



class psg_sales(models.Model):
    _inherit = 'sale.order'


    estimated_hours = fields.Float('Estimated Hours')

    estimated_amps = fields.Float('Estimated Amps')

    maint_type = fields.Selection(
        string='Maintainance Worksheet Required',
        selection=[('none', 'None'),
                   ('default', 'Default Job Sheet'),
                   ('eml', 'Emergency Lighting'),
                   ('access', 'Access Control'),
                   ('cctv', 'CCTV'),
                   ('fire', 'Fire Alarm'),
                   ('int', 'Intruder'),],
        required=False, default='none')