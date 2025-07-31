from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter


from src.library.views.borrow import BorrowViewSet
from src.library.views.author import AuthorViewSet
from src.library.views.category import CategoryViewSet
from src.library.views.library import LibraryStatistic, CreateLibraryMembers
from src.library.views.post import PostViewSet

router = DefaultRouter()
# router = SimpleRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'borrows', BorrowViewSet)
router.register(r'authors', AuthorViewSet)


urlpatterns = [
    path('analytics/library-stats/', LibraryStatistic.as_view()),
    path('<int:library_id>/add_members/', CreateLibraryMembers.as_view()),
    path('books/', include('src.library.urls.books'))
] + router.urls

