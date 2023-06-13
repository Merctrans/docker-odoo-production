from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class InternalUser(models.Model):
    """MercTrans Internal Users"""
    _inherit = ["res.users"]

    contributor = fields.Boolean(string='Contributor', default=False)
    currency = fields.Many2one('res.currency', string='Currency')

    @api.constrains('login')
    def validate_email(self):
        if self.login:
            match = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                self.login)
            if match is None:
                raise ValidationError('Not a valid email')
