from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Count

from src.library.dtos.borrow import BorrowDTO, OverdueBorrowsDTO, TopBorrowerSerializer
from src.library.models import Borrow
from src.users.models import User


class BorrowViewSet(ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowDTO


    @action(methods=["get"], detail=False, url_path="overdue")
    def get_overdue_borrows(self, request):
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