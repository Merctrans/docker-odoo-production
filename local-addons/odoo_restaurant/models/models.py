# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ApplicationUser(models.Model):
    _name = 'tutorial.users'
    _description = 'User for Odoo Tutorial'
    _rec_name = 'first_name'

    #id hidden
    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name')
    email = fields.Char('Email', required=True)
    password = fields.Char('Password')
    department = fields.Many2many('tutorial.department')


class ApplicationDepartment(models.Model):
    _name = 'tutorial.department'
    _description = 'Department for Odoo Tutorial'
    _rec_name = 'name'

    name = fields.Char('Department Name')
    code = fields.Integer('Department Code')
    users = fields.Many2many('tutorial.users')

