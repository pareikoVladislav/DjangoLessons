from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.db.models import Count

from src.library.dtos.borrow import BorrowDTO, OverdueBorrowsDTO, BorrowCreateDTO, TopBorrowerSerializer, BorrowReturnSerializer
from src.library.dtos.library import LibraryRecordCreateDTO, LibraryCreateDTO
from src.library.models import Borrow
from src.permissions.view_permissions import CanGetTopBorrower, IsWorkHour
from src.users.dtos import CreateUserDTO
from src.users.models import User


class BorrowViewSet(ModelViewSet):
    queryset = Borrow.objects.select_related(
        'book'
    ).prefetch_related(
        'library_record__library',
        'library_record__member'
    )
    serializer_class = BorrowDTO

    def get_permissions(self):
        if self.action == 'get_top_borrower':
            return [IsAuthenticated(), CanGetTopBorrower()]
        return [IsAuthenticated(), IsWorkHour()]

    @action(methods=["get"], detail=False, url_path="overdue")
    def get_overdue_borrows(self, request: Request) -> Response:
        queryset = self.queryset.filter(
            is_returned=False,
            return_date__lt=timezone.now().date()
        )
        serializer = OverdueBorrowsDTO(queryset, many=True).data
        return Response(
            data=serializer,
            status=status.HTTP_200_OK
        )
    
    @action(methods=["get"], detail=False, url_path="top-borrowers")
    def get_top_borrower(self, request):
        top_user = (
            User.objects
            .annotate(books_borrowed=Count('borrows__borrows'))
            .order_by('-books_borrowed')
            .filter(books_borrowed__gt=0)
            [:5]
        )

        if not top_user:
            return Response([], status=status.HTTP_200_OK)

        serializer = TopBorrowerSerializer(top_user,many=True)
        return Response([serializer.data], status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_path="create-borrow")
    def create_borrow_record(self, request: Request) -> Response:
        user_data = request.data.get("user")
        lib_data = request.data.get("library")
        borrow_data = request.data.get("borrow")

        if not user_data or not lib_data or not borrow_data:
            raise ValueError("Данные запроса не полные, должны быть пользователь, библиотека, запись займа")

        try:
            transaction.set_autocommit(False)

            # OPERATION #1 Создание пользователя
            user_serializer = CreateUserDTO(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save() # User(...)

            # OPERATION #2 Создание библиотеки
            library_serializer = LibraryCreateDTO(data=lib_data)
            library_serializer.is_valid(raise_exception=True)
            library = library_serializer.save() # Library(...)

            # OPERATION #3 Создание записи в библиотеке
            lib_record_serializer = LibraryRecordCreateDTO(
                data={
                    "library": library.id,
                    "member": user.id,
                }
            )
            lib_record_serializer.is_valid(raise_exception=True)
            lib_record = lib_record_serializer.save() # LibraryRecord(...)


            # OPERATION #4 Создание записи займа
            borrow_data['library_record'] = lib_record.id

            borrow_serializer = BorrowCreateDTO(data=borrow_data)
            borrow_serializer.is_valid(raise_exception=True)
            borrow_serializer.save() # Borrow(...)

            transaction.commit()

            return Response(
                data={
                    "user": user_serializer.data,
                    "library": library_serializer.data,
                    "borrow": borrow_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            transaction.rollback()

            return Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            transaction.set_autocommit(True)

    @action(methods=["post"], detail=True, url_path="return")
    def return_borrow(self, request: Request,pk: int) -> Response:
        try:
            borrow = get_object_or_404(Borrow,pk=pk)
            if borrow.is_returned:
                raise ValueError("Книга уже возвращена")

            with transaction.atomic():
                borrow.return_date = timezone.now().date()
                borrow.is_returned = True
                borrow.save()

                serializer = BorrowReturnSerializer(borrow)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                data={
                    'borrow': f"ошибка: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
