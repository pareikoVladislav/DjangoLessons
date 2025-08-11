from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from src.users.dtos import ListUsersDTO, DetailedUserDTO, CreateUserDTO
from src.users.models import User


class UsersListAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['last_name', 'gender', 'role']
    search_fields = ['username', 'email']
    ordering_fields = ['age', 'is_staff', 'date_joined']


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListUsersDTO
        return CreateUserDTO

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['include_related'] = self.request.query_params.get(
            'include_related',
            'false'
        ).lower() == 'true'

        return context


class UserRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'username'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DetailedUserDTO
        return CreateUserDTO

