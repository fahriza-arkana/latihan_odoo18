# -*- coding: utf-8 -*-
# from odoo import http


# class AspLibrary(http.Controller):
#     @http.route('/asp_library/asp_library', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asp_library/asp_library/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('asp_library.listing', {
#             'root': '/asp_library/asp_library',
#             'objects': http.request.env['asp_library.asp_library'].search([]),
#         })

#     @http.route('/asp_library/asp_library/objects/<model("asp_library.asp_library"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asp_library.object', {
#             'object': obj
#         })

