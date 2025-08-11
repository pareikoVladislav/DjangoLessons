from django.urls import path

from src.users.views import (
    UsersListAPIView,
    UserRetrieveAPIView,
    LoginUserAPIView
)

urlpatterns = [
    path('', UsersListAPIView.as_view()),
    path('auth-login/', LoginUserAPIView.as_view()),
    path('<str:username>/', UserRetrieveAPIView.as_view()),
]
