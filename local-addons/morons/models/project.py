# -*- coding: utf-8 -*-

from odoo import models, fields, api

""""TODO
- Inherit to project.project
- User Project to generate metadata
- Task to delegate tasks to Contributors

"""


class MercTransServices(models.Model):
    _name = 'merctrans.services'
    _rec_name = 'services_names'
    _description = 'Services offered by MercTrans'

    department_list = [('localization', 'Localization'),
                       ('marketing', 'Marketing'),
                       ('development', 'Development')]
    department = fields.Selection(string="Department",
                                  selection=department_list)
    services_names = fields.Char('Services')


class MerctransProject(models.Model):
    _inherit = ['project.project']

    work_unit_list = [('word', 'Word'),
                      ('hour', 'Hour'),
                      ('page', 'Page'),
                      ('job', 'Job')]

    # project_status_list = [('potential', 'Potential'),
    #                        ('confirmed', 'Confirmed'),
    #                        ('in progress', 'In Progress'), ('in qa', 'In QA'),
    #                        ('delivered', 'Delivered'),
    #                        ('canceled', 'Canceled')]

    payment_status_list = [('unpaid', 'Unpaid'), ('invoiced', 'Invoiced'),
                           ('paid', 'Paid')]

    job_id = fields.Integer('Job ID')

    # services contain tags
    project_manager_id = fields.Many2one('res.users', string='Project Manager')
    service = fields.Many2many('merctrans.services', string='Services')
    source_language = fields.Many2one('res.lang', string='Source Language')
    target_language = fields.Many2one('res.lang', string='Target Language')
    discount = fields.Integer('Discount (%)')

    # add discount field
    # fixed job

    work_unit = fields.Selection(string='Work Unit', selection=work_unit_list)
    volume = fields.Integer('Project Volume')
    currency_id = fields.Many2one('res.currency', string='Currency')
    sale_rate = fields.Float('Sale Rate')
    job_value = fields.Monetary("Job Value",
                                compute="_compute_job_value",
                                currency_field='currency_id',
                                store=True,
                                readonly=True)
    # project_status = fields.Selection(string='Project Status',
    #                                   selection=project_status_list)
    payment_status = fields.Selection(string='Payment Status',
                                      selection=payment_status_list)

    @api.depends('volume', 'sale_rate', 'discount')
    def _compute_job_value(self):
        for project in self:
            project.job_value = (100 - project.discount) / 100 * project.volume * project.sale_rate


class MerctransTask(models.Model):
    _inherit = 'project.task'

    po_status_list = [('in progress', 'In Progress'),
                      ('completed', 'Completed'),
                      ('canceled', 'Canceled')]

    work_unit_list = [('word', 'Word'),
                      ('hour', 'Hour'),
                      ('page', 'Page'),
                      ('job', 'Job')]

    payment_status_list = [('unpaid', 'Unpaid'),
                           ('invoiced', 'Invoiced'),
                           ('paid', 'Paid')]

    rate = fields.Float(string='Rate', required=True, default=0)
    service = fields.Many2many('merctrans.services')
    source_language = fields.Many2one('res.lang', string='Source Language')
    target_language = fields.Many2one('res.lang', string='Target Language')
    volume = fields.Integer(string='Volume*', required=True, default=0)
    po_value = fields.Float("PO Value",
                            compute="_compute_po_value",
                            store=True,
                            readonly=True,
                            default=0)
    payment_status = fields.Selection(string='Payment Status*',
                                      selection=payment_status_list,
                                      required=True,
                                      default='unpaid')

    @api.onchange('volume', 'rate')
    @api.depends('volume', 'rate')
    def _compute_po_value(self):
        for project in self:
            project.po_value = (100 - 0) / 100 * project.volume * project.rate
