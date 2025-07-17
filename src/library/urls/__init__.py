from django.urls import path, include


urlpatterns = [
    path('books/', include('src.library.urls.books')),
]
