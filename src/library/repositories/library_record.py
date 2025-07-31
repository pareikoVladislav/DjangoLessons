from src.library.models import LibraryRecord
from src.shared.base_repo import BaseRepository


class LibraryRecordRepository(BaseRepository):
    def __init__(self):
        super().__init__(LibraryRecord)
