from django.urls import path, include

urlpatterns = [
    path('library/', include('src.library.urls')),
]
