from dateutil.parser import ParserError, parse, parserinfo
from django_filters import rest_framework as filters


class CreatedAtFilterMixin(filters.FilterSet):
    created_at = filters.DateFilter()
    from_created_at = filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    to_created_at = filters.DateFilter(field_name='created_at', lookup_expr='date__lte')


class ChoiceInFilter(filters.BaseInFilter, filters.ChoiceFilter):
    pass


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class SearchFilter:
    DASH = '-'

    @classmethod
    def get_parse_date(cls, value):
        try:
            if cls.DASH in value:
                parse_date = parse(value)
            else:
                parse_date = parse(value, parserinfo=parserinfo(dayfirst=True))
            parse_date = parse_date.date()
        except (ParserError, TypeError, OverflowError):
            parse_date = None
        return parse_date
