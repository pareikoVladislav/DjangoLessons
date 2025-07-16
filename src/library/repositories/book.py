from src.library.models import Book
from src.library.repositories.base import BaseRepository


class BookRepository(BaseRepository):
    def __init__(self):
        super().__init__(Book)
