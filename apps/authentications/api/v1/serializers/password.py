from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from apps.services.password_services import PasswordService
from apps.users.models import User


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(
        max_length=128, write_only=True, style={'input_type': 'password'}, required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
        self.password_service = PasswordService()

    def validate_old_password(self, old_password):
        try:
            self.password_service.check_password(self.user, old_password)
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(e)
        return old_password

    def validate_new_password(self, new_password):
        try:
            self.password_service.validate_password(new_password, user=self.user)
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(e)
        return new_password

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if old_password == new_password:
            raise ValidationError('Old and new passwords are the same')
        if confirm_password and new_password != confirm_password:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        assert False, 'Do not use update directly'

    def update(self, instance, validated_data):
        assert False, 'Do not use update directly'

    def save(self, **kwargs):
        self.password_service.change_password(self.user, self.validated_data['new_password'])


class PasswordResetLinkViaEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise exceptions.NotFound()
        validated_data = super().validate(attrs)
        validated_data['user'] = user
        return validated_data


class PasswordResetLinkConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'})
    password_service = PasswordService

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise exceptions.ValidationError('The token is not Valid or Expired')
        if new_password != confirm_password:
            raise ValidationError('Passwords do not match')
        try:
            self.password_service.validate_password(new_password, user=user)
        except ValidationError as e:
            raise exceptions.ValidationError(e) from e
        attrs['user'] = user
        return attrs

    def save(self, user, **kwargs):
        self.password_service.change_password(user, self.validated_data['new_password'])
