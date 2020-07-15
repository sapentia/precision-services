# -*- coding: utf-8 -*-
# from odoo import http


# class Psg(http.Controller):
#     @http.route('/psg/psg/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/psg/psg/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('psg.listing', {
#             'root': '/psg/psg',
#             'objects': http.request.env['psg.psg'].search([]),
#         })

#     @http.route('/psg/psg/objects/<model("psg.psg"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('psg.object', {
#             'object': obj
#         })
