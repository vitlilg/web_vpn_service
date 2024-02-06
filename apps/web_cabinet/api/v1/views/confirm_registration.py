from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models.statement_registration import CustomerStatementRegistration, SecurityCode
from apps.users.tasks.registration import registration_from_statement
from apps.web_cabinet.api.v1.serializers.confirm_registration import ConfirmSailorRegistrationSerializer


class ConfirmCustomerRegistrationView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ConfirmSailorRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        statement = CustomerStatementRegistration.objects.get(
            email=email,
            status=CustomerStatementRegistration.Status.WAITING_CONFIRMATION_EMAIL.value,
        )
        SecurityCode.objects.filter(email=email).delete()
        registration_from_statement.s(statement.pk).apply_async()
        return Response({'status': 'success'})
