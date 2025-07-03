from django.utils import timezone

from django.db import models

class Borrow(models.Model):
    book: models.ForeignKey = models.ForeignKey(
        'Book',
        on_delete=models.PROTECT,
        related_name='books'
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
        if not self.is_returned and timezone.now() > self.return_date:
            return True
        return False

class LibraryRecord(models.Model):
    member: models.ForeignKey = models.ForeignKey(
        'Member',
        on_delete=models.PROTECT,  # если пользователь что-то взял, то пока он не вернет, нельзя удалить))
        related_name='borrows'
    )
    library: models.ForeignKey = models.ForeignKey(
        'Library',
        on_delete=models.PROTECT,
        related_name='borrows'
    )

    @property
    def is_completed(self):
        return all(borrow.is_returned for borrow in self.borrows)
