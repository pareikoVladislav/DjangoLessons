from django.urls import path

from src.users.views import UsersListAPIView, UserRetrieveAPIView

urlpatterns = [
    path('', UsersListAPIView.as_view()),
    path('<int:user_id>/', UserRetrieveAPIView.as_view()),
]
