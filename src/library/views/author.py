from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.library.dtos.author import AuthorDTO
from src.library.models import Author


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorDTO

    @action(methods=['get'], detail=False, url_path='count')
    def count_authors(self, request):
        return Response(
            {
                'count': self.queryset.count()
            },
            status=200
        )
