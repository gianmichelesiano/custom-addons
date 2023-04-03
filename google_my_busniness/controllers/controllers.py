# -*- coding: utf-8 -*-
# from odoo import http


# class GoogleMyBusniness(http.Controller):
#     @http.route('/google_my_busniness/google_my_busniness', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/google_my_busniness/google_my_busniness/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('google_my_busniness.listing', {
#             'root': '/google_my_busniness/google_my_busniness',
#             'objects': http.request.env['google_my_busniness.google_my_busniness'].search([]),
#         })

#     @http.route('/google_my_busniness/google_my_busniness/objects/<model("google_my_busniness.google_my_busniness"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('google_my_busniness.object', {
#             'object': obj
#         })
