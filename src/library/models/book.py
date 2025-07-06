from django.core.validators import MaxValueValidator
from django.db import models

from src.choices.base import Genre, Language


class Book(models.Model):

    title = models.CharField(
        max_length=65
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    genre = models.CharField(
        max_length=50,
        choices=Genre.choices(),
        default=Genre.N_A,
    )
    pages = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)],
    )
    language = models.CharField(
        max_length=20,
        choices=Language.choices(),
        default=Language.en
    )
    published_date = models.DateField(
        auto_now_add=True,
    )
    publisher: models.ForeignKey = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )
    author: models.ForeignKey = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    category: models.ForeignKey = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='books',
        null=True
    )

    libraries= models.ManyToManyField(
        "Library",
        related_name='books',
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        # db_table = "books"
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-published_date', 'title']
        # indexes = [
        #     models.Index(
        #         fields=['genre', 'language'],
        #         name='book_genre_lang_idx'
        #     )
        # ]

        unique_together = ('title', 'published_date')

        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['title', 'published_date'],
        #         name='title_pub_date_unq_cnstrt'
        #     ),
        #     models.CheckConstraint(
        #         check=models.Q(pages__gte=1),
        #         name='book_pages_gte_1_chk_cnstrt'
        #     )
        # ]
        # permissions = []

        # abstract = True

        get_latest_by = '-published_date'
