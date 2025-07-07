from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]}."

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"