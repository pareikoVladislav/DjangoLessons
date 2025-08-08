from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import IsAdminUser
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
            permission_classes=[IsAdminUser]
        ),
        name='swagger-ui'
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(
            url_name='schema',
            permission_classes=[IsAdminUser]
        ),
        name='redoc'
    ),

    path('api/v1/', include('src.routes')),
]
