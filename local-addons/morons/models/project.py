# -*- coding: utf-8 -*-

from odoo import models, fields, api

""""TODO
- Inherit to project.project
- User Project to generate metadata
- Task to delegate tasks to Contributors

"""


class MercTransServices(models.Model):
    _name = "merctrans.services"
    _rec_name = "name"
    _description = "Services offered by MercTrans"

    department_list = [
        ("localization", "Localization"),
        ("marketing", "Marketing"),
        ("development", "Development"),
    ]
    department = fields.Selection(string="Department", selection=department_list)
    name = fields.Char("Services")


class MerctransProject(models.Model):
    _inherit = ["project.project"]

    work_unit_list = [
        ("word", "Word"),
        ("hour", "Hour"),
        ("page", "Page"),
        ("job", "Job"),
    ]

    # project_status_list = [('potential', 'Potential'),
    #                        ('confirmed', 'Confirmed'),
    #                        ('in progress', 'In Progress'), ('in qa', 'In QA'),
    #                        ('delivered', 'Delivered'),
    #                        ('canceled', 'Canceled')]

    payment_status_list = [
        ("unpaid", "Unpaid"),
        ("invoiced", "Invoiced"),
        ("paid", "Paid"),
    ]

    job_id = fields.Char(
        "Project Id",
        default=lambda self: "New",
        readonly=True,
        index=True,
        required=True,
        copy=False,
    )

    # services contain tags

    service = fields.Many2many("merctrans.services", string="Services")
    source_language = fields.Many2one("res.lang", string="Source Language")
    target_language = fields.Many2many("res.lang", string="Target Language")
    discount = fields.Integer("Discount (%)")

    # add discount field
    # fixed job

    work_unit = fields.Selection(string="Work Unit", selection=work_unit_list)
    volume = fields.Integer("Project Volume")
    currency_id = fields.Many2one(
        "res.currency", string="Currency*", required=True, readonly=False
    )
    sale_rate = fields.Float("Sale Rate")
    job_value = fields.Monetary(
        "Project Value",
        compute="_compute_job_value",
        currency_field="currency_id",
        store=True,
        readonly=True,
    )
    # project_status = fields.Selection(string='Project Status',
    #                                   selection=project_status_list)
    payment_status = fields.Selection(string='Payment Status',
                                      selection=payment_status_list)
    po_value = fields.Monetary("PO Value",
                               compute="_compute_po_value",
                               currency_field='currency_id',
                               store=True,
                               readonly=True)
    margin = fields.Float("Project Margin", compute="_compute_margin", store=True, readonly=True)
    receivable = fields.Monetary("Receivable", compute="_compute_receivable")
    # receivable_in_USD = fields.Monte

    @api.model
    def create(self, vals):
        if vals.get("job_id", "New") == "New":
            vals["job_id"] = self.env["ir.sequence"].next_by_code(
                "increment_project_id"
            )

        return super(MerctransProject, self).create(vals)

    @api.depends("volume", "sale_rate", "discount")
    def _compute_job_value(self):
        for project in self:
            project.job_value = (
                    (100 - project.discount) / 100 * project.volume * project.sale_rate
            )

    @api.depends('tasks')
    def _compute_po_value(self):
        for project in self:
            if project.tasks:
                project.po_value = sum(po.po_value for po in project.tasks)

    @api.depends('po_value', 'job_value')
    def _compute_margin(self):
        for project in self:
            if project.job_value and project.po_value:
                project.margin = (project.job_value - project.po_value) / project.job_value

    @api.depends('po_value', 'job_value')
    def _compute_receivable(self):
        for project in self:
            if project.po_value and project.job_value:
                project.receivable = project.job_value - project.po_value
            else:
                project.receivable = 0


class MerctransTask(models.Model):
    _inherit = "project.task"

    po_status_list = [
        ("in progress", "In Progress"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    work_unit_list = [
        ("word", "Word"),
        ("hour", "Hour"),
        ("page", "Page"),
        ("job", "Job"),
    ]

    payment_status_list = [
        ("unpaid", "Unpaid"),
        ("invoiced", "Invoiced"),
        ("paid", "Paid"),
    ]

    rate = fields.Float(string="Rate", required=True, default=0)
    service = fields.Many2many("merctrans.services")
    source_language = fields.Many2one(
        "res.lang",
        string="Source Language",
        compute="_get_source_lang",
        inverse="_invert_get_source_lang",
    )
    target_language = fields.Many2one(
        "res.lang",
        string="Target Language",
    )
    volume = fields.Integer(string="Volume*", required=True, default=0)
    po_value = fields.Float(
        "PO Value", compute="_compute_po_value", store=True, readonly=True, default=0
    )
    payment_status = fields.Selection(
        string="Payment Status*",
        selection=payment_status_list,
        required=True,
        default="unpaid",
    )

    currency = fields.Char('Currency', compute='_compute_currency_id')

    def _invert_get_source_lang(self):
        pass

    def _invert_get_target_lang(self):
        pass

    @api.onchange("volume", "rate")
    @api.depends("volume", "rate")
    def _compute_po_value(self):
        for task in self:
            task.po_value = (100 - 0) / 100 * task.volume * task.rate

    @api.depends("project_id")
    def _get_source_lang(self):
        for task in self:
            if self.project_id:
                self.source_language = self.project_id.source_language

    @api.onchange("user_ids")
    def _compute_currency_id(self):
        for record in self:
            if record.user_ids:
                record.currency = record.user_ids.currency.name
