from django.urls import path

from src.users.views import (
    UsersListAPIView,
    UserRetrieveAPIView,
    LoginUserAPIView,
    LogoutUserAPIView
)

urlpatterns = [
    path('', UsersListAPIView.as_view()),
    path('login/', LoginUserAPIView.as_view()),
    path('logout/', LogoutUserAPIView.as_view()),
    path('<str:username>/', UserRetrieveAPIView.as_view()),
]
