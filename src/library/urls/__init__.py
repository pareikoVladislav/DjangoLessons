from django.urls import path, include


urlpatterns = [
    path('books/', include('src.library.urls.books')),
    path('categories/', include('src.library.urls.categories')), # Добавляем этот маршрут
]
