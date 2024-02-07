from rest_framework import exceptions, serializers

from apps.websites.models import Website


class WebsitesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Website
        fields = ('id', 'name', 'url', 'description', 'created_at', 'is_active')
        read_only_fields = ('created_at',)

    def validate_name(self, value):
        user = self.context['request'].user
        if Website.objects.filter(name=value, customer=user).exists():
            raise exceptions.ValidationError('You have already website with this name.')
        return value
