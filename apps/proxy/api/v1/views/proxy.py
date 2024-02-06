from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.proxy.api.v1.serializers.proxy import ProxySerializer


class ProxyView(GenericAPIView):
    serializer_class = ProxySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
