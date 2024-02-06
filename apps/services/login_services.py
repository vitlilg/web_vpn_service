from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

import utils
from apps.authentications.models.token import Token
from apps.users.models import User


class LoginService:

    @classmethod
    def login(cls, user, request, domain_name=None):
        return cls.get_general_response(user, request)

    @classmethod
    def logout(cls, request):
        request.auth.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @staticmethod
    def set_last_login(user: User):
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return user

    @classmethod
    def create_token(cls, user: User, request):
        client_ip = utils.get_client_ip(request)
        device_info = utils.get_client_device_info(request)
        cls.set_last_login(user)
        Token.objects.filter(
            Q(user=user) &
            Q(
                Q(expiry__gte=timezone.now()) |
                Q(expiry__isnull=True),
            ),
        ).update(
            expiry=timezone.now(),
        )
        return Token.objects.create(
            user=user,
            ip_address=client_ip,
            device_info=device_info,
        )

    @classmethod
    def get_general_response(cls, user: User, request):
        token = cls.create_token(user, request)
        return Response(
            {
                'type': 'general',
                'token': token.key,
            }, status=status.HTTP_200_OK,
        )
