from datetime import timedelta

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.users.exceptions import MissedLinkUrlAttributeError
from apps.users.models import User
from apps.users.models.statement_registration import SecurityCode
from generic.utils.url_processing import ends_with_slash_in_link


class EmailService:
    create_new_password_link_url = 'set-new-password-by-token'

    @staticmethod
    def get_or_create_security_code_for_email(email: str):
        code, created = SecurityCode.objects.get_or_create(email=email)
        if not created:
            time_end_security_code = timezone.now() - timedelta(minutes=30)
            if code.created_at < time_end_security_code:
                code.delete()
                code = SecurityCode.objects.create(email=email)
            else:
                code.created_at = timezone.now()
                code.save(update_fields=['created_at'])
        return code.security_code

    @classmethod
    def create_new_password_link(cls, director_user: User):
        token = PasswordResetTokenGenerator().make_token(director_user)
        link = cls._build_new_password_email_link(director_user, token)
        return link

    @classmethod
    def _build_new_password_email_link(cls, user: User, token: str) -> str:
        if not cls.create_new_password_link_url:
            raise MissedLinkUrlAttributeError
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link_url = ends_with_slash_in_link(cls.create_new_password_link_url)
        email_link = f'{link_url}?token={token}&uid={uid}'
        try:
            validate = URLValidator()
            validate(email_link)
        except DjangoValidationError:
            host_url = ends_with_slash_in_link(settings.FRONT_DOMAIN)
            email_link = f'{host_url}{email_link}'
        return email_link
