from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.users.models import User
from apps.users.models.statement_registration import CustomerStatementRegistration
from apps.users.tasks.users_send_email import get_and_send_security_code_to_email
from apps.web_cabinet.exceptions import CustomerStatementRegistrationValidateEmailFieldError


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerStatementRegistration
        fields = (
            'first_name', 'last_name', 'email', 'status', 'password',
        )
        extra_kwargs = {'status': {'required': False}}

    @staticmethod
    def validate_email(value):
        CustomerStatementRegistration.objects.filter(
            email=value,
            status=CustomerStatementRegistration.Status.WAITING_CONFIRMATION_EMAIL,
        ).update(status=CustomerStatementRegistration.Status.CANCELED)
        if (
                CustomerStatementRegistration.objects.filter(
                    email=value,
                    status=CustomerStatementRegistration.Status.APPROVED,
                ).exists() or
                User.objects.filter(email=value).exists()
        ):
            raise CustomerStatementRegistrationValidateEmailFieldError
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.pop('password'))
        statement = super().create(validated_data)
        get_and_send_security_code_to_email.s(email=statement.email).apply_async()
        return statement
