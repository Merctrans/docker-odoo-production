# -*- coding: utf-8 -*-

from odoo import models, fields, api

""""TODO
- Inherit to project.project
- User Project to generate metadata
- Task to delegate tasks to Contributors

"""


class MercTransServices(models.Model):
    """
    A model representing the different services offered by MercTrans.

    This class encapsulates the various services that MercTrans provides, 
    categorized into different departments. It serves as a way to manage 
    and access the services information in an organized manner.

    Attributes:
        _name (str): Internal name of the model in the Odoo framework.
        _rec_name (str): Field to use for record name.
        _description (str): A brief description of the model's purpose.
        department_list (list of tuples): A predefined list of departments.
        department (fields.Selection): Field for selecting a department from the department_list.
        name (fields.Char): Field for the name of the service.
    """

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
    """
    A model representing projects managed by MercTrans.

    This class extends the functionality of the 'project.project' model 
    to cater specifically to the needs of MercTrans projects. It includes 
    features such as different work units, payment statuses, and calculation 
    of project values and margins. It also handles the creation of unique 
    project IDs and the computation of various financial metrics.

    Attributes:
        _inherit (list): Inherited model name in the Odoo framework.
        work_unit_list (list of tuples): A predefined list of work units for projects.
        payment_status_list (list of tuples): A predefined list of payment statuses.
        job_id (fields.Char): Field for the unique project identifier.
        service (fields.Many2many): Relationship to the 'merctrans.services' model.
        source_language (fields.Many2one): Field for the source language of the project.
        target_language (fields.Many2many): Field for the target languages of the project.
        discount (fields.Integer): Field for any discount applied to the project.
        work_unit (fields.Selection): Field for selecting a work unit from the work_unit_list.
        volume (fields.Integer): Field for the volume of the project.
        currency_id (fields.Many2one): Field for the currency used in the project.
        sale_rate (fields.Float): Field for the sale rate of the project.
        job_value (fields.Monetary): Computed field for the total value of the project.
        payment_status (fields.Selection): Field for the payment status of the project.
        po_value (fields.Monetary): Computed field for the Purchase Order value of the project.
        margin (fields.Float): Computed field for the margin of the project.

    Methods:
        create(vals): Creates a new project with a unique ID.
        _compute_job_value(): Computes the job value based on volume, sale rate, and discount.
        _compute_po_value(): Computes the PO value from all associated tasks.
        _compute_margin(): Calculates the project margin.
        _compute_receivable(): Calculates the receivable of the project.
    """

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
    # receivable = fields.Monetary("Receivable", compute="_compute_receivable")
    # receivable_in_USD = fields.Monte

    @api.model
    def create(self, vals):
        """Creates a new project.

            This method creates a new project and assigns it a unique project ID. 
            It is automatically triggered when a new project is created.

            Parameters:
                vals: A dictionary containing the values of the fields on the project.

            Returns:
                project: The newly created project.
        """
        if vals.get("job_id", "New") == "New":
            vals["job_id"] = self.env["ir.sequence"].next_by_code(
                "increment_project_id"
            )

        return super(MerctransProject, self).create(vals)

    @api.depends("volume", "sale_rate", "discount")
    def _compute_job_value(self):
        """Computes the job value of the project.

            Parameters:
                volume: The volume of the project.
                sale_rate: The sale rate of the project.
                discount: The discount of the project (if any).

            Returns:
                None: Updates the 'job_value' field of each project record with the calculated job value.
        """
        for project in self:
            project.job_value = (
                    (100 - project.discount) / 100 * project.volume * project.sale_rate
            )

    @api.depends('tasks')
    def _compute_po_value(self):
        """Computes the total Purchase Order (PO) value of the project.

            Parameters:
                tasks: The tasks associated with the project.

            Returns:
                None: Updates the 'po_value' field of each project record with the calculated sum.
        """
        for project in self:
            if project.tasks:
                project.po_value = sum(po.po_value for po in project.tasks)

    @api.depends('po_value', 'job_value')
    def _compute_margin(self):
        """Computes the margin of the project.

            Parameters:
                po_value: The total PO value of the project.
                job_value: The total job value of the project.

            Returns:
                None: Updates the 'margin' field of each project record with the calculated margin.
        """
        for project in self:
            if project.job_value and project.po_value:
                project.margin = (project.job_value - project.po_value) / project.job_value

    @api.depends('po_value', 'job_value')
    def _compute_receivable(self):
        """Computes the receivable of the project.

            Parameters:
                po_value: The total PO value of the project.
                job_value: The total job value of the project.

            Returns:
                None: Updates the 'receivable' field of each project record with the calculated receivable.
        """
        for project in self:
            if project.po_value and project.job_value:
                project.receivable = project.job_value - project.po_value
            else:
                project.receivable = 0


class MerctransTask(models.Model):
    """
    A model representing tasks within Merctrans projects.

    This class extends the 'project.task' model of Odoo, tailored for the specific needs of 
    Merctrans projects. It includes functionality for managing purchase order statuses, work units, 
    payment statuses, and various other task-related details. Key features include the ability to 
    compute the value of tasks based on volume and rate, and handling the source and target languages 
    for tasks in translation projects.

    Attributes:
        _inherit (str): Inherited model name in the Odoo framework.
        po_status_list (list of tuples): A predefined list of possible statuses for purchase orders.
        work_unit_list (list of tuples): A predefined list of work units applicable to tasks.
        payment_status_list (list of tuples): A predefined list of payment statuses for tasks.
        rate (fields.Float): Field for the rate applicable to the task.
        service (fields.Many2many): Relationship to the 'merctrans.services' model, indicating services involved in the task.
        source_language (fields.Many2one): Computed field for the source language of the task, derived from the associated project.
        target_language (fields.Many2many): Field for the target languages of the task.
        work_unit (fields.Selection): Field for selecting a work unit from the work_unit_list.
        volume (fields.Integer): Field for the volume of work associated with the task.
        po_value (fields.Float): Computed field for the Purchase Order value of the task.
        payment_status (fields.Selection): Field for the payment status of the task.
        currency (fields.Char): Computed field for the currency used in the task.

    Methods:
        _invert_get_source_lang(): Placeholder method for inverse computation of source language. (TODO)
        _invert_get_target_lang(): Placeholder method for inverse computation of target language.  (TODO)
        _compute_po_value(): Computes the Purchase Order value of the task based on volume and rate.
        _get_source_lang(): Computes the source language of the task based on its associated project.
        _compute_currency_id(): Computes the currency used in the task based on the users assigned to it.
    """
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
    target_language = fields.Many2many(
        "res.lang",
        string="Target Language",
    )
    work_unit = fields.Selection(string="Work Unit", selection=work_unit_list, required=True)
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

    