# -*- coding: utf-8 -*-

from odoo import models, fields, api


class psg_products(models.Model):
    _inherit = 'product.template'

    sec_grade = fields.Integer('Security Grade')
    env_class = fields.Char('Environmental Class')
    applies_to_ids = fields.Char('Applies to')
    install = fields.Float('Installation Faction')
    amps = fields.Float('Amp Rating')




class psg_applications(models.Model):
    _name = 'psg.application'
    _description = 'Application'

    name = fields.Char('Application')
    active = fields.Boolean('Active')
    product_id = fields.Char('Product')