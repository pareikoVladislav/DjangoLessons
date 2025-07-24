from django.urls import path

from src.library.views.category import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    # URL /api/v1/library/categories/ для получения списка категорий и создания новой
    path('', CategoryListCreateAPIView.as_view(), name='category-list-create'),

    # URL /api/v1/library/categories/<title>/ для получения, обновления и удаления кат по назв
    path('<str:title>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-retrieve-update-destroy'),
]