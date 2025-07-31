from rest_framework.viewsets import ModelViewSet

from src.library.models import Post
from src.library.dtos.post import PostDTO
from rest_framework.permissions import IsAuthenticated


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDTO
    permission_classes = [IsAuthenticated]