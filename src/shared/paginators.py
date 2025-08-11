from rest_framework.pagination import CursorPagination, PageNumberPagination


class CustomPageNumber(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomCursorPaginator(CursorPagination):
    page_size = 10
    ordering = '-rating'
