# -*- coding: utf-8 -*-

from odoo import models, fields, api


class psg_contract(models.Model):
    _name = 'psg.contract'
    _description = 'Contracts'

    name = fields.Char('Contract Number')

