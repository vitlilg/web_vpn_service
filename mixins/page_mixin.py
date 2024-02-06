from collections import OrderedDict
from math import ceil

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class ShortLinkResultPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.get_full_path()[1:]
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.get_full_path()[1:]
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('current', self.page.number),
                ('previous', self.get_previous_link()),
                ('total_pages', self.page.paginator.num_pages),
                ('results', data),
            ]),
        )


class StatisticListPaginationMixin:
    current_page: int | None = None
    page_size: int | None = None
    page_query_param = 'page_size'
    num_pages: int | None = None

    def paginated_response(self, request, response_list):
        self.current_page = request.query_params.get('page', 1)
        self.page_size = request.query_params.get('page_size', 20)
        self.num_pages = ceil(len(response_list) / self.validated_page_size())
        start_split = (self.validated_current_page() - 1) * self.validated_page_size()
        end_split = self.validated_current_page() * self.validated_page_size()
        paginated_response = OrderedDict()
        paginated_response['total_pages'] = self.num_pages
        paginated_response['next'] = self.get_next_link()
        paginated_response['current'] = self.validated_current_page()
        paginated_response['previous'] = self.get_previous_link()
        paginated_response['results'] = response_list[start_split:end_split]
        paginated_response['count'] = len(response_list)
        return paginated_response

    def get_next_link(self):
        if self.validated_current_page() >= self.num_pages:
            return None
        url = self.request.get_full_path()[1:]
        page_number = self.validated_current_page() + 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if self.validated_current_page() <= 1:
            return None
        url = self.request.get_full_path()[1:]
        page_number = self.validated_current_page() - 1
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def validated_current_page(self):
        number_to_validate = self.current_page
        number = self.validate_number(number_to_validate)
        return number

    def validated_page_size(self, check_page_size=True):
        number_to_validate = self.page_size
        number = self.validate_number(number_to_validate, check_page_size)
        return number

    def validate_number(self, number, check_page_size=False):
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise ValueError('The page number is not an integer')
        if number < 1:
            raise ValueError('That page number is less than 1')
        if not check_page_size and number > self.num_pages:
            if number == 1:
                pass
            else:
                raise ValueError('That page contains no results')
        return number
