from django.db import models
from django.utils import timezone


class DateTimesMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-modified_at']


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
