from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.core.validators import URLValidator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from rest_framework import exceptions

from apps.authentications.models.token import Token
from apps.users.models import User


class PasswordService:
    @classmethod
    def change_password(cls, user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save(update_fields=['password'])

    @staticmethod
    def check_password(user: User, password: str) -> None:
        if not user.check_password(password):
            raise exceptions.ValidationError('Incorrect password.')

    @staticmethod
    def validate_password(password, user=None) -> None:
        try:
            password_validation.validate_password(password, user=user)
        except DjangoValidationError as e:
            raise exceptions.ValidationError(e.messages) from e


class PasswordRecoveryService:

    @classmethod
    def send_email_password_recovery(cls, request, user, link_url):
        token = PasswordResetTokenGenerator().make_token(user)
        link = cls.build_email_link(request, link_url, user, token)
        context = cls.build_email_context(link, user, request)
        email = cls.get_email(user)
        cls.send_email(email=email, template_context=context)
        return True

    @classmethod
    def build_email_link(cls, request, link_url, user: User, token: Token) -> str:
        uid = cls.get_uid(user)
        email_link = f'{link_url}?token={token}&uid={uid}'
        try:
            validate = URLValidator()
            validate(email_link)
        except DjangoValidationError:
            email_link = request.build_absolute_uri(email_link)
        return email_link

    @staticmethod
    def build_email_context(link, user, request, **kwargs) -> dict:
        return {
            'link': link,
            'user': user.username,
        }

    @staticmethod
    def get_uid(user):
        return urlsafe_base64_encode(force_bytes(user.pk))

    @classmethod
    def get_email(cls, user):
        return getattr(user, user.EMAIL_FIELD)

    @classmethod
    def send_email(cls, email, template_context):
        """
        override this for custom template
        """
        html_message = render_to_string('templates/recovery_password_email.html', template_context)
        from_email, to = settings.DEFAULT_FROM_EMAIL, email
        plain_message = strip_tags(html_message)
        title = 'Password recovery'
        send_mail(title, plain_message, from_email, [to], html_message=html_message)
        return True
