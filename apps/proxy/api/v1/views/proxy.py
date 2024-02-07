from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.history.tasks.history import create_history
from apps.services.base_api_service import RequestService
from apps.websites.models import Website


class ProxyView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        query_params = request.query_params
        website_url = query_params.get('website_url')
        website_name = query_params.get('website_name')
        website = Website.objects.get(name=website_name, customer=user)
        response = RequestService.get(url=website_url)
        create_history.s(
            website_id=website.pk,
            webpage_size=len(response.content),
            webpage=response.url,
        ).apply_async()
        response_headers = {
            'Location': f'{settings.HOST_API_DOMAIN}/api/v1/proxy/?website_name={website_name}&'
                        f'website_url={response.url}',
        }
        return Response(response.content, status=status.HTTP_200_OK, headers=response_headers)
