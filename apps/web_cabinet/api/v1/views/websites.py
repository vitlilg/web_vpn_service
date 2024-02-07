from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.history.tasks.history import create_history
from apps.services.base_api_service import RequestService
from apps.services.user_services import CustomerService
from apps.websites.api.v1.views.websites import BaseWebsiteViewSet


class CabinetWebsiteView(viewsets.ModelViewSet, BaseWebsiteViewSet):

    def perform_create(self, serializer):
        user = CustomerService.get_customer_user_by_request(self.request, self.kwargs)
        serializer.save(customer=user)

    @action(
        methods=['POST'],
        detail=True,
    )
    def follow_to_website(self, request, *args, **kwargs):
        website = self.get_object()
        token = request.auth.key
        headers = self.get_headers(token)
        response = self.website_to_proxy(
            website_url=website.url, website_name=website.name, headers=headers,
        )
        webpage_size = len(response.content)
        create_history.s(
            website_id=website.pk,
            webpage_size=webpage_size,
            webpage=website.url,
        ).apply_async()
        response_headers = {'Location': f'{response.url}'}
        return Response(response.content, status=status.HTTP_200_OK, headers=response_headers)

    def get_headers(self, token):
        return {'Authorization': f'Token {token}'}

    def website_to_proxy(self, website_url: str, website_name: str, headers: dict):
        url = f'{settings.HOST_API_DOMAIN}/api/v1/proxy/?website_name={website_name}&website_url={website_url}'
        return RequestService.get(url=url, headers=headers)
