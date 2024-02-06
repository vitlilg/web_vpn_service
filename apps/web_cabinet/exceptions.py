from rest_framework import exceptions


class CustomerStatementRegistrationValidateEmailFieldError(exceptions.ValidationError):
    default_detail = 'Email is used'


class ConfirmCustomerStatementRegistrationValidateEmailFieldError(exceptions.ValidationError):
    default_detail = 'Statement with this email does not exists'


class InvalidSecurityCodeError(exceptions.ValidationError):
    default_detail = {
        'security_code': 'Security code is invalid',
    }
