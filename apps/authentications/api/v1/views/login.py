import os

from django.utils import timezone
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.authentications.api.v1.serializers.login import EmailSerializer
from apps.authentications.models.token import Token
from apps.authentications.permissions import IsNotAuthenticated
from apps.services.login_services import LoginService
from apps.users.models import User


class LoginView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = EmailSerializer

    def get_origin(self, request):
        app_id = os.getenv('FRONT_DOMAIN', None)
        if not app_id:
            app_id = request.build_absolute_uri('/')[:-1]
        return app_id

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data.get('user')
        expiry = timezone.now()
        Token.objects.filter(user=user, expiry__gte=expiry).update(expiry=expiry)
        response = LoginService.login(user, request, self.get_origin(request))
        return response


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = LoginService.logout(request)
        return response
