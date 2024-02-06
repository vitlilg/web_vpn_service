from django.conf import settings
from rest_framework import viewsets
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
        response = self.proxy_to_website(website_url=website.url, website_name=website.name, headers=headers)
        webpage_size = len(response.content)
        create_history.s(
            website_id=website.pk,
            webpage_size=webpage_size,
            webpage=website.url,
        ).apply_async()
        return Response(response.content)

    def get_headers(self, token):
        return {'Authorization': f'Token {token}'}

    def proxy_to_website(self, website_url: str, website_name: str, headers: dict):
        url = f'{settings.HOST_API_DOMAIN}/api/v1/proxy/'
        json = {
            'website_name': website_name,
            'website_url': website_url,
        }
        return RequestService.post(url=url, headers=headers, json=json)
