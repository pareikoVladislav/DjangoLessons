from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from src.users.service import UserService
from src.users.dtos import ListUsersDTO, DetailedUserDTO, CreateUserDTO
from src.users.models import User

# # Базовая работа Django
# # class UsersListAPIView(GenericAPIView):
# #     serializer_class = ListUsersDTO
# #     queryset = User.objects.all()
# #
# #     def get(self, request: Request) -> Response:
# #         queryset = self.get_queryset()
# #         serializer = self.get_serializer(queryset, many=True)
# #
# #         return Response(
# #             data=serializer.data,
# #             status=status.HTTP_200_OK
# #         )
#
#
#
# # Работа через сервисы и репозитории
# class UsersListAPIView(GenericAPIView):
#     # serializer_class = ListUsersDTO
#     service = UserService
#
#     def get_queryset(self):
#         service = self.service()
#
#         response = service.get_all_users()
#
#         if not response.success:
#             raise Exception(response.message)
#
#         return response.data
#
#     def get(self, request: Request) -> Response:
#         queryset = self.get_queryset()
#
#         return Response(
#             data=queryset,
#             status=status.HTTP_200_OK
#         )
#
#
# class UserRetrieveAPIView(GenericAPIView):
#     serializer_class = DetailedUserDTO
#     service = UserService
#     lookup_url_kwarg = 'user_id'
#
#     def get_object(self):
#         service = self.service()
#         user_id = self.kwargs.get('user_id')
#
#         response = service.get_user_by_id(user_id)
#
#         if not response.success:
#             raise Exception(response.message)
#
#         return response.data
#
#     def get(self, request: Request, *args, **kwargs) -> Response:
#         user = self.get_object()
#         return Response(
#             data=user,
#             status=status.HTTP_200_OK
#         )


class UsersListAPIView(ListCreateAPIView):
    # serializer_class = ListUsersDTO
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
    # lookup_field = 'username'
    lookup_url_kwarg = 'username'
    # username = url dynamic param <>

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DetailedUserDTO
        return CreateUserDTO

