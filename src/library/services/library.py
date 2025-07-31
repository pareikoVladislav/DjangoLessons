from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction

from src.library.dtos.statistics import LibraryStatisticDTO
from src.library.repositories.library import LibraryRepository
from src.library.repositories.library_record import LibraryRecordRepository
from src.users.repository import UserRepository


class LibraryService:
    def __init__(self):
        self.library_repo = LibraryRepository()
        self.user_repo = UserRepository()
        self.library_record_repo = LibraryRecordRepository()

    def get_statistic_by_library(self, query_params):
        try:
            statistic = {
                "books_count": self.library_repo.get_books_count_per_library(),
                "most_popular_books": self.library_repo.get_most_popular_books_per_library(query_params),
                "count_books_per_genre": self.library_repo.count_books_per_genre(),
                "top_genres": self.library_repo.get_top_genres_per_library(query_params),
                "count_readers": self.library_repo.count_readers(),
                "top_readers": self.library_repo.get_top_readers(),
                "top_active_weekdays": self.library_repo.get_most_active_weekdays()
            }
            serializer = LibraryStatisticDTO(statistic).data
            return serializer

        except DatabaseError as e:
            return f"Database Error: {str(e)}"

    def create_new_members(
            self,
            library_id: int,
            user_data_list: list[dict[str, Any]]
    ) -> list:
        try:
            transaction.set_autocommit(False)

            library = self.library_repo.get_by_id(library_id)
            if not library:
                raise ObjectDoesNotExist(f"Library with id {library_id} not found.")

            created_users = []
            for user_data in user_data_list:
                user = self.user_repo.create(**user_data)
                self.library_record_repo.create(
                    library_id=library.id,
                    member_id=user.id
                )
                created_users.append(user)

            transaction.commit()
            return created_users

        except Exception as e:
            transaction.rollback()
            raise

        finally:
            transaction.set_autocommit(True)
