from django.db.models import Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters

from apps.users.models import User
from mixins.filters_mixin import ChoiceInFilter


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    full_name = filters.CharFilter(method='full_name_filter')
    type_user = ChoiceInFilter(choices=User.TypeUserChoices.choices)

    def full_name_filter(self, queryset, name, value):
        queryset = queryset.alias(
            full_name=Concat('last_name', Value(' '), 'first_name'),
        )
        return queryset.filter(full_name__icontains=value)

    ordering = filters.OrderingFilter(
        fields=(
            ('email', 'email'),
        ),
    )
