from django.db import models

from mixins.model_mixin import DateTimesMixin, IsActiveMixin


class Website(DateTimesMixin, IsActiveMixin):
    name = models.CharField(max_length=256, help_text='Website name')
    url = models.URLField(help_text='Website URL')
    description = models.TextField(default='')
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='customer_websites')

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'
        ordering = ['-id']
