from enum import Enum
from django.core.validators import MaxValueValidator
from django.db import models

LAN_CHOICES = [
    ('en', 'English'),
    ('be', 'Belarusian'),
    ('ru', 'Russian')
]

class Genre(str, Enum):
    N_A = 'N/A'
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    SCIENCE_FICTION = 'Science Fiction'
    FANTASY = 'Fantasy'
    MYSTERY = 'Mystery'
    BIOGRAPHY = 'Biography'

    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]


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
        null=True,
        blank=True
    )
    pages = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)],
        null=True,
        blank=True
    )
    language = models.CharField(
        max_length=20,
        choices=LAN_CHOICES,
        # null=True,
        default=LAN_CHOICES[0][0]
    )
    published_date = models.DateField(
        auto_now_add=True,
    )
    publisher: models.ForeignKey = models.ForeignKey(
        'Publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    def __str__(self):
        return f"{self.title}({self.published_date})"


# Наш senior посмотрел на модель, что мы создали и предложил внести некоторые правки по улучшению модели.
#
# В модель Book добавьте дополнительные поля для большей информации о книге:
#
# Краткое описание: TextField, может быть пустым
# Жанр: CharField, макс. длина 50, выборы из ['Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Biography']
# Кол-во страниц: может быть пустым, максимальное кол-во - 10000
#
# Примените изменения в модели, попробуйте создать записи, не указывая некоторые поля. Обратите внимание на то, как отрабатывает система.