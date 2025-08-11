from django.db.models import Count
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from src.library.dtos.category import CategoryDTO
from src.library.models import Category
from src.permissions import CategoryStaffWritePermission


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryDTO
    permission_classes = [CategoryStaffWritePermission]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']

    @action(methods=['get'], detail=False, url_path='statistic')
    def get_category_statistic(self, request: Request) -> Response:
        qs = Category.objects.annotate(
            books_count=Count('books')
        )

        data = [
            {
                'id': obj.id,
                'title': obj.title,
                'books_count': obj.books_count,
            }
            for obj in qs
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path='custom-method')
    def custom_method(self, request: Request) -> Response:
        return Response(
            data={'message': 'Custom method works!'},
        )
