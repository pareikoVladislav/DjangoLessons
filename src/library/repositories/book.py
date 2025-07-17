from src.library.models import Book
from src.library.repositories.base import BaseRepository


class BookRepository(BaseRepository):
    def __init__(self):
        super().__init__(Book)

    def create_book_with_libraries(self, **kwargs):
        obj = self.model.objects.create(**kwargs)

        obj.libraries.set(kwargs.pop('libraries'))

        return obj
