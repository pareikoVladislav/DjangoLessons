from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from src.library.models.managers.author import SoftDeleteAuthorManager


class Author(models.Model):
    first_name: str = models.CharField(
        max_length=100,
        verbose_name='Имя',
    )
    last_name:str = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
    )
    birth_date: datetime = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )
    profile = models.URLField(
        max_length=80,
        null=True,
        blank=True,
        verbose_name='Ссылка на профиль',
        help_text='Вставить валидный URL'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен или нет',
        help_text='True = Автор активен, False = Автор неактивен\\удален'
    )
    rating: float = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0)
        ],
        default=1.0,
        verbose_name='Рейтинг',
    )
    deleted = models.BooleanField(
        default=False
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    objects = SoftDeleteAuthorManager()

    def delete(self, using = None, keep_parents = False):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]}."
