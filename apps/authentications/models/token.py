import binascii
import os

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.users.models import User


class Token(models.Model):
    key = models.CharField(
        max_length=settings.AUTH_TOKEN_CHARACTER_LENGTH,
        db_index=True,
        primary_key=True,
    )
    user = models.ForeignKey(
        User,
        related_name='auth_token_set',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    device_info = models.CharField(max_length=525, blank=True, default='')
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f'{self.key} : {self.user}, {self.device_info}'

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None,
    ):
        if not self.key:
            self.key = self.generate_key()
        expiry = settings.TOKEN_TTL
        if not self.expiry and expiry:
            self.expiry = timezone.now() + expiry

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    @property
    def is_expire(self):
        return self.expiry and self.expiry < timezone.now()

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(int(settings.AUTH_TOKEN_CHARACTER_LENGTH / 2))).decode()
