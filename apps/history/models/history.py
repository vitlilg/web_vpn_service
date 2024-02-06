from django.db import models
from django.utils import timezone


class History(models.Model):

    created_at = models.DateTimeField(default=timezone.now, help_text='Website follow date and time')
    website = models.ForeignKey(
        'websites.Website', on_delete=models.CASCADE, help_text='Website to', related_name='website_history',
        null=True,
    )
    webpage = models.TextField(default='', help_text='Full webpage link')
    webpage_size = models.IntegerField(help_text='Webpage data size')

    class Meta:
        verbose_name = 'Website following history'
        ordering = ['-id']
