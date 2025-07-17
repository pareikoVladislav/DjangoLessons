from django.urls import path

from src.library.views.book import (
    get_all_books,
    get_book_by_id,
    create_book,
    update_book,
    delete_book
)


urlpatterns = [
    path('', get_all_books),
    path('create/', create_book),
    path('<int:book_id>', get_book_by_id),
    path('<int:book_id>/update', update_book),
    path('<int:book_id>/delete', delete_book),
]
