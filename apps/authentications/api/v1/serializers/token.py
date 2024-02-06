from rest_framework import serializers

from apps.authentications.models.token import Token
from apps.users.models import User


class TokenSerializer(serializers.ModelSerializer):
    is_current_session = serializers.SerializerMethodField()
    pk_md5 = serializers.ReadOnlyField()

    class Meta:
        model = Token
        fields = ('created_at', 'expiry', 'last_activity', 'device_info', 'ip_address', 'is_current_session', 'pk_md5')

    def get_is_current_session(self, instance: Token):
        request = self.context.get('request')
        if not request:
            return False
        auth_token = request.auth
        return isinstance(auth_token, Token) and auth_token == instance


class TokenVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'type_user']
        read_only_fields = fields
