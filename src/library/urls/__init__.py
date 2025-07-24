from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from src.library.views.category import CategoryViewSet
from src.library.views.post import PostViewSet

router = DefaultRouter()
# router = SimpleRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('books/', include('src.library.urls.books')),
] + router.urls

