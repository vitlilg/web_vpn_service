from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.services.user_services import CustomerService
from apps.users.models import User
from apps.websites.api.v1.serializers.websites import WebsitesSerializer
from apps.websites.models import Website
from apps.websites.permissions import WebsitePermissions
from mixins.views_mixin import ListSerializerClassMixin


class BaseWebsiteViewSet(
    ListSerializerClassMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [WebsitePermissions]
    queryset = Website.objects.all()
    serializer_class = WebsitesSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_queryset().none()
        user = CustomerService.get_customer_user_by_request(self.request, self.kwargs)
        if user.type_user == User.TypeUserChoices.CUSTOMER:
            return super().get_queryset().filter(customer=user)
        elif user.type_user == User.TypeUserChoices.ADMIN:
            return super().get_queryset().all()
        return super().get_queryset().none()


class WebsiteViewSet(BaseWebsiteViewSet):
    pass
