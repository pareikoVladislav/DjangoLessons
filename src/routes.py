from django.urls import path, include

urlpatterns = [
    path('library/', include('src.library.urls')),
    path('users/', include('src.users.urls')),
]
