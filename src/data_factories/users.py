from __future__ import annotations

import random
from datetime import date
from typing import Iterable

import factory
from factory import LazyAttribute
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDate

from src.choices.base import Role
from src.data_factories.libraries import LibraryFactory
from src.users.models import User
from src.library.models import Library, LibrariesMembers

from django.utils import timezone


def choices_values(enum_class) -> list[str]:
    raw = list(enum_class.choices())

    if raw and isinstance(raw[0], (list, tuple)):
        return [c[0] for c in raw]

    return raw


def now_tz():
    return timezone.now()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email')


    username = factory.Faker('user_name', locale="en_US")
    first_name = factory.Faker('first_name', locale="en_US")
    last_name = factory.Faker('last_name', locale="en_US")
    email = factory.Faker('email', locale="en_US")
    phone = factory.Faker('phone_number')
    gender = FuzzyChoice(['male', 'female'])
    birth_date = FuzzyDate(date(1950, 1, 1), date(2023, 9, 1))
    age = LazyAttribute(
        lambda obj: max(6, min(120, int((date.today() - obj.birth_date).days // 365)))
    )
    role = FuzzyChoice(choices_values(Role))
    is_active = True
    is_staff = False

    password = factory.PostGenerationMethodCall("set_password", "password123")


    # Заполняем M2M-связи пользователя с библиотеками через явную through-модель.
    @factory.post_generation
    def libraries(self, create, extracted: Iterable[Library] | None, **kwargs):
        if not create:
            return
        # Если библиотеки переданы — создаём through-записи для каждой.
        if extracted:
            for lib in extracted:
                LibrariesMembersFactory(member=self, library=lib)
        # Иначе по умолчанию подключаем к 1-2 новым библиотекам.
        else:
            # Создаём случайно 1 или 2 библиотеки.
            for lib in LibraryFactory.create_batch(random.randint(1, 2)):
                LibrariesMembersFactory(member=self, library=lib)


class LibrariesMembersFactory(DjangoModelFactory):
    class Meta:
        model = LibrariesMembers

    library = factory.SubFactory(LibraryFactory)
    member = factory.SubFactory(UserFactory)
