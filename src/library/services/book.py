from typing import Dict, Any

from django.db import IntegrityError
from rest_framework.serializers import ValidationError
from rest_framework.pagination import PageNumberPagination

from src.library.dtos.book import BookListDTO, BookDetailedDTO, BookCreateDTO
from src.library.repositories.book import BookRepository
from src.shared.base_service_response import ServiceResponse, ErrorType


class BookService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.paginator = PageNumberPagination()
        self.paginator.page_size = 5
        self.paginator.page_size_query_param = 'page_size'

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')

        if page_size and page_size.isdigit():
            return int(page_size)

        return self.paginator.page_size

    def get_all_books(self, request, query_params) -> ServiceResponse:
        try:
            page_size = self.get_page_size(request)
            self.paginator.page_size = page_size

            books_queryset = self.book_repo.get_all_with_params(query_params)

            results = self.paginator.paginate_queryset(books_queryset, request, view=None)

            # books_queryset
            """
            {
                "obj_count": books_queryset.count(),
                "cur_page": <cur page>,
                "prev": <prev link>,
                "next": <next link>,
                "results": [
                    **book_queryset
                ],
            }
            """
            serializer = BookListDTO(results, many=True)

            resp = self.paginator.get_paginated_response(serializer.data)

            return ServiceResponse(
                success=True,
                data=resp.data
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
