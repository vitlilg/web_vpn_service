from rest_framework import serializers

from apps.users.models import User, UserProfile


class UserProfileInfoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'middle_name', 'photo',
        )
        read_only_fields = fields

    def get_photo(self, instance):
        request = self.context.get('request')
        if instance.photo:
            return request.build_absolute_uri(instance.photo.url)
        return None


class UserInfoSerializer(serializers.ModelSerializer):
    userprofile = UserProfileInfoSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'type_user', 'userprofile', 'email')
