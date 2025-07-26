import calendar

from django.db.models import Count, Q, F
from django.db import DatabaseError, OperationalError
from django.db.models.functions import ExtractWeekDay

from src.choices.base import Role
from src.library.models import Library, Book
from src.library.repositories.book import BookRepository
from src.library.repositories.borrow import BorrowRepository
from src.shared.base_repo import BaseRepository
from src.users.models import User


class LibraryRepository(BaseRepository):
    book_repo = BookRepository()
    borrow_repo = BorrowRepository()

    def __init__(self):
        super().__init__(Library)

    def get_books_count_per_library(self):
        try:
            # books_queryset = self.get_all_with_params(query_params)
            # return books_queryset.values(
            #     library=F("libraries__name")).annotate(
            #     count_books=Count("id", distinct=True))
            return self.model.objects.values(library=F("name")).annotate(count_books=Count('books'))
        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    def get_most_popular_books_per_library(self, query_params):
        books_queryset = self.book_repo.get_all_with_params(query_params)

        try:
            library_queryset = self.model.objects.all()
            top_books_per_library = {}

            for library in library_queryset:
                top_books = (books_queryset
                             .filter(libraries=library)
                             .annotate(borrows_count=Count("borrows"))
                             .order_by("-borrows_count")[:5]
                             )
                top_books_per_library[library.name] = top_books

            return top_books_per_library

        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    def get_top_genres_per_library(self, query_params):
        books = self.book_repo.get_all_with_params(query_params)
        try:
            library_queryset = self.model.objects.all()
            top_genres_per_library = {}
            for library in library_queryset:
                count_borrows = books.filter(libraries=library).values("genre").annotate(
                    count_borrows=Count("borrows")).order_by("-count_borrows")[:3]
                top_genres_per_library[library.name] = count_borrows
            return top_genres_per_library

        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    def count_readers(self):
        try:
            return self.model.objects.all().values(
                "name").annotate(count_readers=Count(
                "members", filter=Q(members__role=Role.reader))
            )

        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    def get_top_readers(self):
        try:
            libraries = self.model.objects.all()
            top_readers_per_library = {}

            for library in libraries:
                top_readers = User.objects.filter(
                    role=Role.reader,
                    libraries=library
                ).values("username").annotate(count_borrows=Count(
                    "library_records__borrows")).order_by("-count_borrows")[:10]
                top_readers_per_library[library.name] = top_readers

            return top_readers_per_library

        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    def get_most_active_weekdays(self):
        try:
            libraries = self.model.objects.all()
            top_active_weekdays_per_library = {}

            for library in libraries:
                top_active_weekdays = self.borrow_repo.model.objects.filter(library_record__library=library).annotate(
                    weekday=ExtractWeekDay("borrow_date")).values("weekday").annotate(
                    count_borrows=Count("id")).order_by("-count_borrows")[:2]
                top_active_weekdays_per_library[library.name] = top_active_weekdays

            return top_active_weekdays_per_library

        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    def count_books_per_genre(self):
        books = Book.objects.all()
        try:
            library_queryset = self.model.objects.all()
            count_books_by_genre_in_library = {}
            for library in library_queryset:
                count_books_per_genre = books.filter(
                    libraries=library).values("genre").annotate(count_books=Count("id"))
                count_books_by_genre_in_library[library.name] = count_books_per_genre
            return count_books_by_genre_in_library

        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e
