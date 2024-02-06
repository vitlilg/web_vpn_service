from difflib import SequenceMatcher

from django.contrib.auth import password_validation
from django.core import exceptions as django_exceptions
from django.core.validators import validate_email
from rest_framework import exceptions, serializers

from apps.users.api.v1.serializers.user_profile import UserProfileSerializer
from apps.users.exceptions import TooSimilarPasswordError, UserValidateEmailFieldError
from apps.users.models import User, UserProfile
from apps.users.tasks.users_send_email import send_email_about_successful_registration


class ListUserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'is_active', 'type_user', 'userprofile',
        )
        read_only_fields = fields


class DetailUserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(required=True, partial=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'is_active', 'type_user', 'userprofile',
        )
        read_only_fields = ('last_login',)
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def validate_email(self, value):
        try:
            validate_email(value)
        except django_exceptions.ValidationError as exc:
            raise serializers.ValidationError(', '.join(error for error in exc.messages))
        exists_email = User.objects.filter(email=value).exists()
        if exists_email:
            raise UserValidateEmailFieldError
        return value

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, user=self.instance)
        except django_exceptions.ValidationError as exc:
            raise exceptions.ValidationError(' '.join(error for error in exc.messages))
        return value

    @staticmethod
    def _validate_email_password(attrs):
        password = attrs.get('password')
        email = attrs.get('email')
        if password and email and SequenceMatcher(a=password.lower(), b=email.lower()).quick_ratio() > 0.7:
            raise TooSimilarPasswordError

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile', {})
        validated_data['password'] = password = User.objects.make_random_password(8)
        user = User.objects.create_user(**validated_data)
        if userprofile_data:
            UserProfile.objects.create(
                user=user,
                **userprofile_data,
            )
        send_email_about_successful_registration.s(user, password).apply_async()
        return user

    def update(self, instance, validated_data):
        is_active = validated_data.get('is_active')
        if is_active is not None:
            instance.is_active = is_active
        instance.save()
        return instance


class ChangeUserActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active',)
