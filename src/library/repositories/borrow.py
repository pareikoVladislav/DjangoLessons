from src.library.models import Borrow
from src.shared.base_repo import BaseRepository


class BorrowRepository(BaseRepository):
    def __init__(self):
        super().__init__(Borrow)
