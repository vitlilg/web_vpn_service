from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.authentications.api.v1.serializers.password import (
    ChangePasswordSerializer, PasswordResetLinkConfirmSerializer, PasswordResetLinkViaEmailSerializer,
)
from apps.authentications.tasks.auth_send_email import send_email_about_recovery_password
from apps.services.password_services import PasswordRecoveryService


class ChangePasswordAPIView(CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({'status': 'success'})


class ChangePasswordByTokenView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetLinkConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=serializer.validated_data.get('user'))
        return Response({'status': 'success'})


class SendPasswordRecoveryEmailView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetLinkViaEmailSerializer
    password_recovery_service = PasswordRecoveryService
    link_url = '/set-new-password-by-token'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid()
        except exceptions.NotFound:
            return Response({'status': 'success'})

        user = serializer.validated_data.get('user')
        token = PasswordResetTokenGenerator().make_token(user)

        link = self.password_recovery_service.build_email_link(request, self.link_url, user, token)
        context = self.password_recovery_service.build_email_context(link, user, request)
        self.perform_sending_email(email=getattr(user, user.EMAIL_FIELD), template_context=context)
        return Response({'status': 'success'})

    def perform_sending_email(self, email, template_context):
        send_email_about_recovery_password.s(email, template_context).apply_async()
        return True
