from django.db import DatabaseError, OperationalError

from src.library.models import Book
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

        genre = params.get('genre')
        language = params.get('language')
        category = params.get('category')

        if genre:
            queryset = queryset.filter(genre=genre)

        if language:
            queryset = queryset.filter(language=language)

        if category:
            try:
                queryset = queryset.filter(category_id=int(category))
            except (TypeError, ValueError):
                return self.model.objects.none()

        authors = params.getlist('author')  # {'author': ['Joe', 'Sapkivski', 'King', ...], 'year': '2023'}
        pub_date = params.get('year')

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

        ordering = params.get('ordering')
        if ordering in ('published_date', '-published_date'):
            queryset = queryset.order_by(ordering)

        allowed_sort_params = {'published_date', 'id'}
        sort_by = params.get('sort_by', 'published_date')
        sort_order = params.get('sort_order', 'asc')

        if sort_by not in allowed_sort_params:
            sort_by = 'published_date'
        if sort_order == 'desc':
            sort_by = f"-{sort_by}"

        queryset = queryset.order_by(sort_by)

        return queryset
