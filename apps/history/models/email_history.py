from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class EmailSendingHistory(models.Model):
    class Status(models.TextChoices):
        SUCCESS = 'success'
        ERROR = 'error'

    title = models.CharField(max_length=255)
    from_email = models.EmailField()
    recipients = ArrayField(models.EmailField())
    send_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUCCESS)
    error_type = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'Email sending history'
        ordering = ['-id']
