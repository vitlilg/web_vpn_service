from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models.statement_registration import CustomerStatementRegistration
from apps.web_cabinet.api.v1.serializers.registration import CustomerRegistrationSerializer


class CustomerRegistrationView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomerRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            status=CustomerStatementRegistration.Status.WAITING_CONFIRMATION_EMAIL,
        )
        return Response({
            'description': 'Statement has been created. Code send to email.',
            'status': 'success',
        })
