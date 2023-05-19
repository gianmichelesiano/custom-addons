# -*- coding: utf-8 -*-
# from odoo import http


# class AyrshareLatest(http.Controller):
#     @http.route('/ayrshare_latest/ayrshare_latest', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ayrshare_latest/ayrshare_latest/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ayrshare_latest.listing', {
#             'root': '/ayrshare_latest/ayrshare_latest',
#             'objects': http.request.env['ayrshare_latest.ayrshare_latest'].search([]),
#         })

#     @http.route('/ayrshare_latest/ayrshare_latest/objects/<model("ayrshare_latest.ayrshare_latest"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ayrshare_latest.object', {
#             'object': obj
#         })
