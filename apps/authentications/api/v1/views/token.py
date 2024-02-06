from django.db.models import Case, IntegerField, Value, When
from django.db.models.functions import MD5
from django.utils import timezone
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.authentications.api.v1.serializers.token import TokenSerializer, TokenVerifySerializer
from apps.authentications.models.token import Token


class TokenView(mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Token.objects.all().annotate(
        pk_md5=MD5('key'),
    )
    serializer_class = TokenSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'pk_md5'
    lookup_field = 'pk_md5'

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            expiry__gte=timezone.now(),
        ).annotate(
            ordering=Case(
                When(key=Value(self.request.auth.key), then=Value(1)), default=0, output_field=IntegerField(),
            ),
        ).order_by('-ordering')

    @action(
        methods=['get'],
        detail=False,
        serializer_class=TokenVerifySerializer,
    )
    def verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
