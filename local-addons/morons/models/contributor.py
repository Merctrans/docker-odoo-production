import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import pytz


class InternalUser(models.Model):
    """
    A model for managing internal users at MercTrans.

    This class extends the 'res.users' model from Odoo, specifically tailored for 
    the needs of MercTrans. It includes additional fields to store information 
    about the users' roles, contact details, nationality, payment methods, and 
    educational background. This class is crucial for managing internal users' 
    data, from basic identification details to more specific information like 
    payment methods and educational qualifications.

    Attributes:
        General:
            _inherit (str): Inherited model name in the Odoo framework.
            contributor (fields.Boolean): Field to indicate if the user is a contributor.
            active (fields.Boolean): Field to indicate if the user account is active.
            currency (fields.Many2one): Relation to 'res.currency' to set the user's preferred currency.
            skype (fields.Char): Field for the user's Skype ID.
            nationality (fields.Many2many): Relation to 'res.lang' to represent the user's nationality.
            country_of_residence (fields.Many2one): Relation to 'res.country' for the user's country of residence.
            timezone (fields.Selection): Selection field for the user's timezone.

        Payment Methods:
            paypal (fields.Char): Field for the user's PayPal ID.
            transferwise_id (fields.Char): Field for the user's Wise ID.
            bank_account_number (fields.Char): Field for the user's bank account number.
            bank_name (fields.Char): Field for the name of the user's bank.
            iban (fields.Char): Field for the user's IBAN.
            swift (fields.Char): Field for the user's SWIFT code.
            bank_address (fields.Char): Field for the user's bank address.
            preferred_payment_method (fields.Selection): Selection field for the user's preferred payment method.

        Education and Experience:
            dates_attended (fields.Date): Field for the dates the user attended educational institutions.
            school (fields.Char): Field for the name of the school the user attended.
            field_of_study (fields.Char): Field for the user's field of study.
            year_obtained (fields.Selection): Selection field for the year the user obtained their degree.
            certificate (fields.Char): Field for the name of any certificate obtained by the user.

    Methods:
        _tz_get(): Returns a list of all timezones for the timezone selection field.
        validate_email(): Validates the format of the user's email for PayPal and login.
    """

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
    
    # @api.model
    # def _tz_get(self):
    #     return [(x, x) for x in pytz.all_timezones]
    
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
    
    # @api.constrains('paypal')
    # def validate_email(self):
    #     if self.paypal:
    #         match = re.match(
    #             '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
    #             self.paypal)
    #         if match is None:
    #             raise ValidationError('Not a valid email')
    
    # # Education and Experience
    # dates_attended = fields.Date('Date Attended')
    # school = fields.Char('School')
    # field_of_study = fields.Char('Field of Study')
    # year_obtained = fields.Selection([(num, str(num)) for num in range(1900, datetime.datetime.now().year + 1)], 'Year')
    # certificate = fields.Char('Certificate')
    
    # @api.constrains('login')
    # def validate_email(self):
    #     if self.login:
    #         match = re.match(
    #             '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
    #             self.login)
    #         if match is None:
    #             raise ValidationError('Not a valid email')
