from django.utils import timezone

from django.db import models


class Borrow(models.Model):
    book: models.ForeignKey = models.ForeignKey(
        'Book',
        on_delete=models.PROTECT,
        related_name='borrows'
    )
    borrow_date = models.DateField(
        auto_now_add=True
    )
    return_date = models.DateField()
    is_returned = models.BooleanField(
        default=False
    )
    library_record: models.ForeignKey = models.ForeignKey(
        'LibraryRecord',
        on_delete=models.PROTECT,
        related_name='borrows'
    )

    @property
    def is_overdue(self):
        if self.return_date and not self.is_returned and timezone.now().date() > self.return_date:
            return True
        return False

    def __str__(self):
        return f"Reader {self.book.title} - Book {self.library_record.member.last_name}"


class LibraryRecord(models.Model):
    member: models.ForeignKey = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,  # если пользователь что-то взял, то пока он не вернет, нельзя удалить))
        related_name='library_records'
    )
    library: models.ForeignKey = models.ForeignKey(
        'Library',
        on_delete=models.PROTECT,
        related_name='library_records'
    )

    @property
    def is_completed(self):
        return all(borrow.is_returned for borrow in self.borrows)

    def __str__(self):
        return f"{self.member.last_name} - {self.library.name}"
