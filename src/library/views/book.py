from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.library.services.base_response import ErrorType
from src.library.services.book import BookService
from src.utils.converters import validate_and_convert_choices


@api_view(['GET'])
def get_all_books(request: Request) -> Response:
    books_service = BookService()
    result = books_service.get_all_books()

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


@api_view(['GET'])
def get_book_by_id(request: Request, book_id: int) -> Response:
    books_service = BookService()
    result = books_service.get_book_by_id(book_id)

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


@api_view(['POST'])
def create_book(request: Request) -> Response:
    books_service = BookService()
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

    result = books_service.create_book(book_data)

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


@api_view(['PUT', 'PATCH'])
def update_book(request: Request, book_id: int) -> Response:
    books_service = BookService()
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

    if request.method == 'PATCH':
        result = books_service.update_book(book_id, update_data, partial=True)
    else:
        result = books_service.update_book(book_id, update_data)

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


@api_view(['DELETE'])
def delete_book(request: Request, book_id: int) -> Response:
    books_service = BookService()
    result = books_service.delete_book(book_id)

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
