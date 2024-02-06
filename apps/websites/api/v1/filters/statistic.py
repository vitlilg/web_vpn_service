from django_filters import rest_framework as filters

from apps.history.models.history import History


class WebsiteStatisticFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter(field_name='created_at__date')
    customer = filters.NumberFilter(field_name='website.customer_id')

    class Meta:
        model = History
        fields = ('created_at', 'customer')
