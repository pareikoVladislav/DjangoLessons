from datetime import timezone

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from src.choices.base import Gender, Role


class Library(models.Model):
    name = models.CharField(max_length=255)


class LibraryRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


class Borrow(models.Model):
    library_record = models.ForeignKey(LibraryRecord, on_delete=models.CASCADE)
    borrow_date = models.DateField()


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        max_length=50,
    )
    last_name = models.CharField(
        max_length=50
    )
    email = models.EmailField(
        unique=True,
    )
    phone = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        choices=Gender.choices(),
        max_length=15,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    age = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(6),
            MaxValueValidator(120)
        ],
        null=True,
        blank=True,
    )
    role = models.CharField(
        max_length=50,
        choices=Role.choices(),
        default=Role.reader
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(
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
