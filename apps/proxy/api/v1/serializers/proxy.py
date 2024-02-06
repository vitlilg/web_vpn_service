from rest_framework import serializers


class ProxySerializer(serializers.Serializer):
    website_name = serializers.CharField(max_length=256)
    website_url = serializers.URLField()
