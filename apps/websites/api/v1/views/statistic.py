from django.db.models import F, Q, Sum
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.history.models.history import History
from apps.users.models import User
from apps.websites.api.v1.filters.statistic import WebsiteStatisticFilter
from mixins.page_mixin import StatisticListPaginationMixin


class WebsiteStatisticView(ListAPIView, StatisticListPaginationMixin):
    queryset = History.objects.filter()
    filterset_class = WebsiteStatisticFilter

    def get_queryset(self):
        user: User = self.request.user
        if user.type_user == User.TypeUserChoices.ADMIN:
            return self.queryset.all()
        elif user.type_user == User.TypeUserChoices.CUSTOMER:
            return self.queryset.filter(website__customer=user)
        return self.queryset.none()

    @extend_schema(methods=['GET'], filters=True)
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        websites = queryset.annotate(
            website_name=F('website__name'),
            website_url=F('website__url'),
        ).values('website_id', 'website_name', 'website_url')
        skip_list = []
        response_list = []
        for website in websites:
            if website['website_id'] in skip_list:
                continue
            response_list.append({
                'website_id': website['website_id'],
                'website_name': website['website_name'],
                'website_url': website['website_url'],
                'website_size': queryset.aggregate(
                    website_size=Sum('webpage_size', filter=Q(website_id=website['website_id'])),
                ).get('website_size'),
                'website_count': queryset.filter(website_id=website['website_id']).count(),
            })
            skip_list.append(website['website_id'])
        paginated_response = self.paginated_response(request, response_list)
        return Response(paginated_response, status=status.HTTP_200_OK)
