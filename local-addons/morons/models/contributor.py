import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import pytz


class InternalUser(models.Model):
    """MercTrans Internal Users"""
    _inherit = ["res.users"]

    contributor = fields.Boolean(string='Contributor', default=False)
    active = fields.Boolean(string='Active', default=True)
    currency = fields.Many2one('res.currency', string='Currency')
    # skype = fields.Char(string='Skype')
    # nationality = fields.Many2many('res.lang', required=True)
    # country_of_residence = fields.Many2one('res.country', required=True)
    # timezone = fields.Selection('_tz_get',
    #                             string='Timezone',
    #                             required=True,
    #                             default=lambda self: self.env.user.tz or 'UTC')
    #
    # @api.model
    # def _tz_get(self):
    #     return [(x, x) for x in pytz.all_timezones]
    #
    # # Payment Methods
    # paypal = fields.Char('PayPal ID')
    # transferwise_id = fields.Char('Wise ID')
    # bank_account_number = fields.Char('Bank Account Number')
    # bank_name = fields.Char('Bank Name')
    # iban = fields.Char('IBAN')
    # swift = fields.Char('SWIFT')
    # bank_address = fields.Char('Bank Address')
    # preferred_payment_method = fields.Selection(selection=[('paypal', 'Paypal'),
    #                                                        ('transferwise', 'Wise'),
    #                                                        ('bank', 'Bank Transfer')])
    #
    # @api.constrains('paypal')
    # def validate_email(self):
    #     if self.paypal:
    #         match = re.match(
    #             '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
    #             self.paypal)
    #         if match is None:
    #             raise ValidationError('Not a valid email')
    #
    # # Education and Experience
    # dates_attended = fields.Date('Date Attended')
    # school = fields.Char('School')
    # field_of_study = fields.Char('Field of Study')
    # year_obtained = fields.Selection([(num, str(num)) for num in range(1900, datetime.datetime.now().year + 1)], 'Year')
    # certificate = fields.Char('Certificate')
    #
    # @api.constrains('login')
    # def validate_email(self):
    #     if self.login:
    #         match = re.match(
    #             '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
    #             self.login)
    #         if match is None:
    #             raise ValidationError('Not a valid email')
