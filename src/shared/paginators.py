from rest_framework.pagination import CursorPagination, PageNumberPagination


class CustomPageNumber(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'


class CustomCursorPaginator(CursorPagination):
    page_size = 10
    ordering = '-rating'
