from django.conf import settings
from rest_framework import serializers

from apps.users.exceptions import UserProfileValidatePhotoFieldError
from apps.users.models import UserProfile


class UserProfileUploadPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('photo',)

    def validate_photo(self, value):
        if value.size > settings.MAX_FILES_SIZE_FOR_UPLOAD:
            raise UserProfileValidatePhotoFieldError
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id', 'middle_name', 'photo',
        )

    def get_photo(self, instance):
        request = self.context.get('request')
        if instance.photo:
            return request.build_absolute_uri(instance.photo.url)
        return None


class ShortUserProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'country', 'region', 'city', 'branch_office', 'photo',
        )

    def get_photo(self, instance):
        request = self.context.get('request')
        if instance.photo:
            return request.build_absolute_uri(instance.photo.url)
        return None
