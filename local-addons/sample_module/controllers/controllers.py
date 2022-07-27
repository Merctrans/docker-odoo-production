# -*- coding: utf-8 -*-
# from odoo import http


# class SampleModule(http.Controller):
#     @http.route('/sample_module/sample_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample_module/sample_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample_module.listing', {
#             'root': '/sample_module/sample_module',
#             'objects': http.request.env['sample_module.sample_module'].search([]),
#         })

#     @http.route('/sample_module/sample_module/objects/<model("sample_module.sample_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample_module.object', {
#             'object': obj
#         })
