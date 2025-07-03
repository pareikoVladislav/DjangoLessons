from datetime import datetime
from enum import Enum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Gender(str, Enum):
    male = "Male"
    female = "Female"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class Role(str, Enum):
    admin = "Admin"
    employee = "Employee"
    reader = "Reader"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class LibrariesMembers(models.Model):
    library = models.ForeignKey(
        'Library',
        on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE
    )


class Member(models.Model):
    first_name: str = models.CharField(
        max_length=50,
    )
    last_name: str = models.CharField(
        max_length=50
    )
    email: str = models.EmailField(
        unique=True,
    )
    gender: Gender = models.CharField(
        choices=Gender.choices()
    )
    birth_date: datetime = models.DateField(
        null=True,
        blank=True,
    )
    age: int = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(120)]
    )
    role: Role = models.CharField(
        max_length=50,
        choices=Role.choices(),
        default=Role.reader
    )
    is_active: bool = models.BooleanField(
        default=True,
    )
    libraries = models.ManyToManyField(
        'Library',
        through=LibrariesMembers,
        related_name='members',
    )
