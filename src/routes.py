from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('library/', include('src.library.urls')),
    path('users/', include('src.users.urls')),
    path('auth-login-jwt/', TokenObtainPairView.as_view()),
    path('auth-token-refresh/', TokenRefreshView.as_view()),
]
