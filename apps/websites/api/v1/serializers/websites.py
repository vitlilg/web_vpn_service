from rest_framework import serializers

from apps.websites.models import Website


class WebsitesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Website
        fields = ('id', 'name', 'url', 'description', 'created_at', 'is_active')
        read_only_fields = ('created_at',)
