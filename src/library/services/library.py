from django.db import DatabaseError

from src.library.dtos.statistics import LibraryStatisticDTO
from src.library.repositories.library import LibraryRepository


class LibraryService:
    def __init__(self):
        self.library_repo = LibraryRepository()

    def get_statistic_by_library(self, query_params):
        try:
            statistic = {
                "books_count": self.library_repo.get_books_count_per_library(),
                "most_popular_books": self.library_repo.get_most_popular_books_per_library(query_params),
                "count_books_per_genre": self.library_repo.count_books_per_genre(),
                "top_genres": self.library_repo.get_top_genres_per_library(query_params),
                "count_readers": self.library_repo.count_readers(),
                "top_readers":  self.library_repo.get_top_readers(),
                "top_active_weekdays": self.library_repo.get_most_active_weekdays()
            }
            serializer = LibraryStatisticDTO(statistic).data
            return serializer

        except DatabaseError as e:
            return f"Database Error: {str(e)}"
