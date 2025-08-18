from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Iterable

import factory
from factory import LazyAttribute
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDate

from src.users.models import User
# from django.contrib.auth.models import User
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


    username = factory.Faker('user_name', locale="en_EN")
    first_name = factory.Faker('first_name', locale="en_EN")
    last_name = factory.Faker('last_name', locale="en_EN")
    email = factory.Sequence(lambda o: f"{o.username}@example.com")
    # email = factory.Faker('email', locale="en_EN")
    phone = factory.Faker('phone_number')
    gender = FuzzyChoice(['male', 'female'])
    birth_date = FuzzyDate(date(1950, 1, 1), date(2023, 9, 1))
    age = LazyAttribute(
        lambda obj: max(6, min(120, int((date.today() - obj.birth_date).days // 365)))
    )
