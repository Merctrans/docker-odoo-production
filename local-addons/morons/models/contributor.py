from odoo import models, fields, api


class InternalUser(models.Model):
    """MercTrans Internal Users"""
    _inherit = ["res.users"]

    contributor = fields.Boolean(string='Contributor', default=False)
    currency = fields.Many2one('res.currency', string='Currency')

