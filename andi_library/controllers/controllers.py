# -*- coding: utf-8 -*-
# from odoo import http


# class AndiLibrary(http.Controller):
#     @http.route('/andi_library/andi_library', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/andi_library/andi_library/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('andi_library.listing', {
#             'root': '/andi_library/andi_library',
#             'objects': http.request.env['andi_library.andi_library'].search([]),
#         })

#     @http.route('/andi_library/andi_library/objects/<model("andi_library.andi_library"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('andi_library.object', {
#             'object': obj
#         })

