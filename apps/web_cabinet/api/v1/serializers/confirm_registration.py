from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import serializers

from apps.users.models.statement_registration import CustomerStatementRegistration, SecurityCode
from apps.web_cabinet.exceptions import (
    ConfirmCustomerStatementRegistrationValidateEmailFieldError, InvalidSecurityCodeError,
)


class ConfirmCustomerRegistrationSerializer(serializers.Serializer):
    security_code = serializers.IntegerField()
    email = serializers.EmailField()

    @staticmethod
    def validate_email(value):
        if not CustomerStatementRegistration.objects.filter(
            email=value, status=CustomerStatementRegistration.Status.WAITING_CONFIRMATION_EMAIL,
        ).exists():
            raise ConfirmCustomerStatementRegistrationValidateEmailFieldError
        return value

    def validate(self, attrs):
        security_code_obj = SecurityCode.objects.filter(
            email=attrs['email'],
            security_code=attrs['security_code'],
        ).first()
        if not security_code_obj:
            raise InvalidSecurityCodeError
        if security_code_obj.created_at < timezone.now() - relativedelta(minutes=30):
            security_code_obj.delete()
            raise InvalidSecurityCodeError
        return super().validate(attrs)
