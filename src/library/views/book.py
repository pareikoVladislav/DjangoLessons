from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated


from src.shared.base_service_response import ErrorType
from src.library.services.book import BookService
from src.utils.converters import validate_and_convert_choices


class BookListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    books_service = BookService()

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
    permission_classes = [IsAuthenticated]
    books_service = BookService()

    def get(self, request: Request, book_id: int) -> Response:
        result = self.books_service.get_book_by_id(book_id)

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

        result = self.books_service.update_book(book_id, update_data)

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

        result = self.books_service.update_book(book_id, update_data, partial=True)

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
    def delete(self, request: Request, book_id: int) -> Response:
        result = self.books_service.delete_book(book_id)

        if result.success:
            return Response(
                data={'message': result.message},
                status=status.HTTP_200_OK
            )
        else:
            response_status = (status.HTTP_404_NOT_FOUND
                               if result.error_type == ErrorType.NOT_FOUND
                               else status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(
                data={'error': result.message},
                status=response_status
            )
