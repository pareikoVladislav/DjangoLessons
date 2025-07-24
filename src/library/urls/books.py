from django.urls import path

from src.library.views.book import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    path('', BookListCreateAPIView.as_view()),
    path('<int:book_id>', BookRetrieveUpdateDestroyAPIView.as_view()),
]


# QUERY PARAMS: http://localhost:8000/api/v1/books/?author=Joe
