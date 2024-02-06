import random
from datetime import datetime

from django.db import models

from mixins.model_mixin import DateTimesMixin


class SecurityCode(models.Model):

    security_code = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    email = models.EmailField(null=True)

    def save(self, *args, **kwargs):
        if not self.security_code:
            self.security_code = random.randint(100000, 999999)
        super().save(*args, **kwargs)


class CustomerStatementRegistration(DateTimesMixin):

    class Status(models.IntegerChoices):
        APPROVED = 2, 'Approved'
        CANCELED = 6, 'Cancelled'
        WAITING_CONFIRMATION_EMAIL = 8, 'Waiting confirmation email'

    first_name = models.CharField(
        max_length=100, default='', blank=True, help_text='First name in english',
    )
    last_name = models.CharField(
        max_length=100, default='', blank=True, help_text='Last name in english',
    )
    middle_name = models.CharField(
        max_length=100, default='', blank=True, help_text='Middle name in english',
    )
    status = models.IntegerField(choices=Status.choices)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        null=True,
        related_name='customer_statement_registrations',
    )

    class Meta:
        verbose_name = 'Application for customer registration'

    @property
    def user_full_name(self) -> str:
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()
