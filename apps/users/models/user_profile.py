from django.db import models


def get_company_upload_user_photo_path(instance, filename):
    return f'user_profile/photo/{instance.id}/{filename}'


class UserProfile(models.Model):

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='userprofile')
    middle_name = models.CharField(max_length=150, blank=True, default='')
    photo = models.ImageField(null=True, blank=True, upload_to=get_company_upload_user_photo_path)
