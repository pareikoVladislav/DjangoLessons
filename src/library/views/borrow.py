from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from src.library.dtos.borrow import BorrowDTO, OverdueBorrowsDTO
from src.library.models import Borrow


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