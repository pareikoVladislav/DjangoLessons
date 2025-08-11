from datetime import datetime

from django.contrib.auth import authenticate
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

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


class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        login, password = request.data.get('username'), request.data.get('password')

        try:
            user = authenticate(
                request=request,
                username=login,
                password=password
            )

            if user:
                response = Response(status=status.HTTP_200_OK)


                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                refresh_exp = make_aware(
                    datetime.fromtimestamp(refresh.payload['exp'])
                )
                access_exp = make_aware(
                    datetime.fromtimestamp(access.payload['exp'])
                )

                response.set_cookie(
                    key='refresh',
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    expires=refresh_exp
                )

                response.set_cookie(
                    key='access',
                    value=str(access),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    expires=access_exp
                )

                return response

            else:
                return Response(
                    data={
                        'error': 'Invalid username or password'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                data={
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutUserAPIView(APIView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.COOKIES.get('refresh')

            if refresh_token:
                token = RefreshToken(refresh_token)

                token.blacklist()

            response = Response(status=status.HTTP_200_OK)
        except Exception as e:
            response = Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response
