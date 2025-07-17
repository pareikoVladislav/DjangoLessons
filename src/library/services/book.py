from typing import Dict, Any

from django.db import IntegrityError
from rest_framework.serializers import ValidationError

from src.library.dtos.book import BookListDTO, BookDetailedDTO, BookCreateDTO
from src.library.repositories.book import BookRepository
from src.library.services.base_response import ServiceResponse, ErrorType


class BookService:
    def __init__(self):
        self.book_repo = BookRepository()

    def get_all_books(self) -> ServiceResponse:
        try:
            books_queryset = self.book_repo.get_all()
            serializer = BookListDTO(books_queryset, many=True)

            return ServiceResponse(
                success=True,
                data=serializer.data
            )

        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f"Error retrieving books: {str(e)}",
                error_type=ErrorType.UNKNOWN_ERROR
            )

    def get_book_by_id(self, book_id: int) -> ServiceResponse:
        try:
            book = self.book_repo.get_by_id(book_id)

            if book is None:
                return ServiceResponse(
                    success=False,
                    message=f"Book with ID {book_id} not found",
                    error_type=ErrorType.NOT_FOUND
                )

            serializer = BookDetailedDTO(book)

            return ServiceResponse(
                success=True,
                data=serializer.data
            )

        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f"Error retrieving book: {str(e)}",
                error_type=ErrorType.UNKNOWN_ERROR
            )

    def create_book(self, data: Dict[str, Any]) -> ServiceResponse:
        create_serializer = BookCreateDTO(data=data)

        if not create_serializer.is_valid():
            return ServiceResponse(
                success=False,
                errors=create_serializer.errors,
                message="Validation failed",
                error_type=ErrorType.VALIDATION_ERROR
            )

        try:

            created_book = create_serializer.save() # create()
            response_serializer = BookDetailedDTO(created_book)

            return ServiceResponse(
                success=True,
                data=response_serializer.data,
                message="Book created successfully"
            )

        except IntegrityError as e:
            return ServiceResponse(
                success=False,
                errors={"database": str(e)},
                message="Integrity constraint violation",
                error_type=ErrorType.INTEGRITY_ERROR
            )

        except ValidationError as e:
            return ServiceResponse(
                success=False,
                errors={"validation": str(e)},
                message="Validation error",
                error_type=ErrorType.VALIDATION_ERROR
            )

        except Exception as e:
            return ServiceResponse(
                success=False,
                errors={"unknown": str(e)},
                message="Unexpected error occurred",
                error_type=ErrorType.UNKNOWN_ERROR
            )

    def update_book(self, book_id: int, data: Dict[str, Any], partial: bool = False) -> ServiceResponse:
        if not self.book_exists(book_id):
            return ServiceResponse(
                success=False,
                message=f"Book with ID {book_id} not found",
                error_type=ErrorType.NOT_FOUND
            )

        try:
            dto_data = BookCreateDTO(data=data, partial=partial)
            dto_data.is_valid(raise_exception=True)
            updated_book = self.book_repo.update(book_id, **dto_data.validated_data)

            serializer = BookDetailedDTO(updated_book)

            return ServiceResponse(
                success=True,
                data=serializer.data,
                message="Book updated successfully"
            )

        except ValidationError as e:
            return ServiceResponse(
                success=False,
                errors={"validation": str(e)},
                message="Validation error during update",
                error_type=ErrorType.VALIDATION_ERROR
            )

        except IntegrityError as e:
            return ServiceResponse(
                success=False,
                errors={"database": str(e)},
                message="Integrity constraint violation",
                error_type=ErrorType.INTEGRITY_ERROR
            )

        except Exception as e:
            return ServiceResponse(
                success=False,
                errors={"unknown": str(e)},
                message=f"Error updating book: {str(e)}",
                error_type=ErrorType.UNKNOWN_ERROR
            )

    def delete_book(self, book_id: int) -> ServiceResponse:
        if not self.book_exists(book_id):
            return ServiceResponse(
                success=False,
                message=f"Book with ID {book_id} not found",
                error_type=ErrorType.NOT_FOUND
            )

        try:
            self.book_repo.delete(book_id)

            return ServiceResponse(
                success=True,
                message=f"Book with ID {book_id} deleted successfully"
            )

        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f"Error deleting book: {str(e)}",
                error_type=ErrorType.UNKNOWN_ERROR
            )

    def book_exists(self, book_id: int) -> bool:
        return self.book_repo.get_by_id(book_id) is not None
