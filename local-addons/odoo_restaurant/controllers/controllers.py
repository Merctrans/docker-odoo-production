# -*- coding: utf-8 -*-
# from odoo import http


# class OdooRestaurant(http.Controller):
#     @http.route('/odoo_restaurant/odoo_restaurant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_restaurant/odoo_restaurant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_restaurant.listing', {
#             'root': '/odoo_restaurant/odoo_restaurant',
#             'objects': http.request.env['odoo_restaurant.odoo_restaurant'].search([]),
#         })

#     @http.route('/odoo_restaurant/odoo_restaurant/objects/<model("odoo_restaurant.odoo_restaurant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_restaurant.object', {
#             'object': obj
#         })
