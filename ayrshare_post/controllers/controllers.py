# -*- coding: utf-8 -*-
# from odoo import http


# class AyrsharePost(http.Controller):
#     @http.route('/ayrshare_post/ayrshare_post', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ayrshare_post/ayrshare_post/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ayrshare_post.listing', {
#             'root': '/ayrshare_post/ayrshare_post',
#             'objects': http.request.env['ayrshare_post.ayrshare_post'].search([]),
#         })

#     @http.route('/ayrshare_post/ayrshare_post/objects/<model("ayrshare_post.ayrshare_post"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ayrshare_post.object', {
#             'object': obj
#         })
