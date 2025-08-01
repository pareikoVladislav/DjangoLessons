from datetime import timezone

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from src.choices.base import Gender, Role


class User(AbstractBaseUser, PermissionsMixin):
    username: str = models.CharField(
        max_length=50,
        unique=True,
    )
    first_name: str = models.CharField(
        max_length=50,
    )
    last_name: str = models.CharField(
        max_length=50
    )
    email: str = models.EmailField(
        unique=True,
    )
    phone: str = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )
    gender: Gender = models.CharField(
        choices=Gender.choices(),
        max_length=15,
    )
    birth_date: timezone = models.DateField(
        null=True,
        blank=True,
    )
    age: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(6),
            MaxValueValidator(120)
        ],
        null=True,
        blank=True,
    )
    role: Role = models.CharField(
        max_length=50,
        choices=Role.choices(),
        default=Role.reader
    )
    is_active: bool = models.BooleanField(
        default=True,
    )
    is_staff: bool = models.BooleanField(
        default=False,
    )
    date_joined: timezone = models.DateTimeField(
        auto_now_add=True,
    )
    libraries = models.ManyToManyField(
        'library.Library',
        through='library.LibrariesMembers',
        related_name='members',
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.last_name} {self.first_name[0]}."
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        return ""
