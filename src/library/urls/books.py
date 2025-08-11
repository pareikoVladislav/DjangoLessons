from django.urls import path

from src.library.views.book import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    path('', BookListCreateAPIView.as_view()),
    path('<int:book_id>', BookRetrieveUpdateDestroyAPIView.as_view()),
]
