from django.urls import path

from src.library.views import get_all_categories, create_new_category

urlpatterns = [
    path('categories/', get_all_categories),
    path('categories/create/', create_new_category),
]
