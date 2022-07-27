# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sample_module(models.Model):
#     _name = 'sample_module.sample_module'
#     _description = 'sample_module.sample_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
