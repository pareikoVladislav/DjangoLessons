from django.db import transaction, DatabaseError, IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.library.dtos.author import AuthorDTO, AuthorCreateUpdateDTO
from src.library.models import Author, Book
from src.shared.paginators import CustomCursorPaginator


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorDTO
    pagination_class = CustomCursorPaginator


    @action(methods=['get'], detail=False, url_path='count')
    def count_authors(self, request):
        return Response(
            {
                'count': self.queryset.count()
            },
            status=200
        )

    @action(methods=['post'], detail=False, url_path='create-author-books')
    def create_author_with_books(self, request: Request) -> Response:
        try:
            author_data = request.data.get('author')
            books_data = request.data.get('books', [])

            if not author_data or not isinstance(books_data, list):
                raise ValidationError(
                    {
                        'detail': 'Invalid data provided. Expected "author" and "books_data" keys.'
                    }
                )
            with transaction.atomic():
                # первая операция, создание автора
                author_serializer = AuthorCreateUpdateDTO(data=author_data)
                author_serializer.is_valid(raise_exception=True)
                author = author_serializer.save()


                # вторая операция, создание книг и привязка к созданному автору
                books_to_create = []

                for book in books_data:
                    try:
                        books_to_create.append(Book(author=author, **book))
                    except TypeError as e:
                        raise ValidationError(
                            {
                                'detail': f'Invalid data provided: {str(e)}'
                            }
                        ) from e

                Book.objects.bulk_create(books_to_create)

                return Response(
                    data={
                        'author': author_serializer.data
                    },
                    status=status.HTTP_201_CREATED,
                )


        except ValidationError as e:
            return Response(
                data={
                    'error': e.detail
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as e:
            return Response(
                data={
                    'author': f"Нарушение целостноси данных: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DatabaseError as e:
            return Response(
                data={
                    'author': f"Ошибка базы данных: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                data={
                    'author': f"Серверная ошибка: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
