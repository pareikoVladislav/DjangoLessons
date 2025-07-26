from django.db import DatabaseError, OperationalError
from django.db.models import Count, F

from src.library.models import Book, Library
from src.shared.base_repo import BaseRepository


class BookRepository(BaseRepository):
    def __init__(self):
        super().__init__(Book)

    def get_all_with_params(self, query_params):
        try:
            queryset = self._get_queryset(query_params)
            return queryset
        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    def _get_queryset(self, params):
        allowed_sort_params = {'price', 'published_date'}

        queryset = self.model.objects.all() # SELECT * FROM books;

        authors = params.getlist('author')  # {'author': ['Joe', 'Sapkivski', 'King', ...], 'year': '2023'}
        pub_date = params.get('year')
        sort_by = params.get('sort_by', 'id')
        sort_order = params.get('sort_order', 'asc')

        if authors:
            queryset = queryset.filter(
                author__last_name__in=authors  # SELECT * FROM books WHERE author IN (...);
            )

        if pub_date:
            try:
                year = int(pub_date)
                queryset = queryset.filter(
                    published_date__year=year  # SELECT * FROM books WHERE author IN (...) AND published_date = ...;
                )
            except ValueError:
                queryset = queryset.none()  # QuerySet([])

        if sort_by not in allowed_sort_params:
            sort_by = 'id'

        if sort_order == 'desc':
            sort_by = f"-{sort_by}"

        queryset = queryset.order_by(sort_by)

        return queryset
