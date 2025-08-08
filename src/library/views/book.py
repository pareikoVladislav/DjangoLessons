from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from src.library.dtos.book import BookDetailedDTO, BookCreateDTO, BookListDTO
from src.library.models import Book
from src.permissions import IsOwnerOrReadOnly
from src.shared.base_service_response import ErrorType
from src.library.services.book import BookService
from src.utils.converters import validate_and_convert_choices


class BookListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    books_service = BookService()

    @extend_schema(
        operation_id="get_books_list",
        summary="Get Books",
        responses={
            200: BookListDTO,
            401: OpenApiResponse(description="Unauthorized"),
            500: OpenApiResponse(description="Error")
        },
        tags=["Books"]
    )
    def get(self, request: Request) -> Response:
        query_params = request.query_params

        result = self.books_service.get_all_books(request, query_params)

        if result.success:
            return Response(
                data=result.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'error': result.message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @extend_schema(
        operation_id="create_book",
        summary="Create new Book",
        request=BookCreateDTO,
        responses={
            201: BookDetailedDTO,
            400: OpenApiResponse(description="Invalid data provided"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            500: OpenApiResponse(description="Error")
        },
        tags=["Books"]
    )
    def post(self, request: Request) -> Response:
        book_data = request.data.copy()

        if request.user.is_authenticated:
            book_data['publisher'] = request.user.id

        choice_errors = validate_and_convert_choices(book_data)

        if choice_errors:
            return Response(
                data={
                    'error': 'Invalid choices provided',
                    'errors': choice_errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = self.books_service.create_book(book_data)

        if result.success:
            return Response(
                data={
                    'message': result.message,
                    'book': result.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={
                    'error': result.message,
                    'errors': result.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BookRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    books_service = BookService()

    @extend_schema(
        operation_id="get_book_by_id",
        summary="Get Book",
        responses={
            200: BookDetailedDTO,
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found")
        },
        tags=["Books"]
    )
    def get(self, request: Request, book_id: int) -> Response:
        result = self.books_service.get_book_by_id(
            book_id,
            request,
            self.permission_classes
        )

        if result.success:
            return Response(
                data=result.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'error': result.message,
                    'errors': result.errors
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        operation_id="update_book_by_id",
        summary="Update Book",
        request=BookCreateDTO,
        responses={
            200: BookDetailedDTO,
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Invalid data provided"),
            500: OpenApiResponse(description="Error")
        },
        tags=["Books"]
    )
    def put(self, request: Request, book_id: int) -> Response:
        update_data = request.data.copy()

        choice_errors = validate_and_convert_choices(update_data)
        if choice_errors:
            return Response(
                data={
                    'error': 'Invalid choices provided',
                    'errors': choice_errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = self.books_service.update_book(
            book_id,
            update_data,
            self.permission_classes,
            request,
        )

        if result.success:
            return Response(
                data={
                    'message': result.message,
                    'book': result.data
                },
                status=status.HTTP_200_OK
            )
        else:
            if result.error_type == ErrorType.NOT_FOUND:
                response_status = status.HTTP_404_NOT_FOUND
            elif result.error_type in [ErrorType.VALIDATION_ERROR, ErrorType.INTEGRITY_ERROR]:
                response_status = status.HTTP_400_BAD_REQUEST
            else:
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response(
                data={
                    'error': result.message,
                    'errors': result.errors,
                    'error_type': result.error_type.value if result.error_type else None
                },
                status=response_status
            )

    @extend_schema(
        operation_id="update_book_by_id",
        summary="Update Book",
        request=BookCreateDTO,
        responses={
            200: BookDetailedDTO,
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Invalid data provided"),
            500: OpenApiResponse(description="Error")
        },
        tags=["Books"]
    )
    def patch(self, request: Request, book_id: int) -> Response:
        update_data = request.data.copy()

        choice_errors = validate_and_convert_choices(update_data)
        if choice_errors:
            return Response(
                data={
                    'error': 'Invalid choices provided',
                    'errors': choice_errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = self.books_service.update_book(
            book_id,
            update_data,
            self.permission_classes,
            request,
            partial=True
        )

        if result.success:
            return Response(
                data={
                    'message': result.message,
                    'book': result.data
                },
                status=status.HTTP_200_OK
            )
        else:
            if result.error_type == ErrorType.NOT_FOUND:
                response_status = status.HTTP_404_NOT_FOUND
            elif result.error_type in [ErrorType.VALIDATION_ERROR, ErrorType.INTEGRITY_ERROR]:
                response_status = status.HTTP_400_BAD_REQUEST
            else:
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response(
                data={
                    'error': result.message,
                    'errors': result.errors,
                    'error_type': result.error_type.value if result.error_type else None
                },
                status=response_status
            )

    @extend_schema(
        operation_id="delete_book_by_id",
        summary="Delete Book",
        responses={
            200: OpenApiResponse(description="Book Deleted Successfully"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
            500: OpenApiResponse(description="Error")
        },
        tags=["Books"]
    )
    def delete(self, request: Request, book_id: int) -> Response:
        result = self.books_service.delete_book(
            book_id,
            request,
            self.permission_classes,
        )

        if result.success:
            return Response(
                data={'message': result.message},
                status=status.HTTP_200_OK
            )
        else:
            if result.error_type == ErrorType.NOT_FOUND:
                response_status = status.HTTP_404_NOT_FOUND
            elif result.error_type == ErrorType.FORBIDDEN:
                response_status = status.HTTP_403_FORBIDDEN
            else:
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response(
                data={'error': result.message},
                status=response_status
            )
