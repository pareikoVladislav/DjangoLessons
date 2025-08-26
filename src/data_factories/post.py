from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone as dt_timezone

import factory
from django.utils import timezone
from factory import LazyAttribute, Sequence
from factory.fuzzy import FuzzyChoice, FuzzyDateTime
from factory.django import DjangoModelFactory

from src.data_factories.libraries import LibraryFactory
from src.data_factories.users import UserFactory
from src.library.models import Post


def now_tz() -> datetime:
    return timezone.now()


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Sequence(lambda n: f"Новость библиотеки #{n}")
    content = factory.Faker("paragraph", nb_sentences=6, locale="en_US")
    author = factory.SubFactory(UserFactory)
    library = factory.SubFactory(LibraryFactory)

    created_at = FuzzyDateTime(
        start_dt=datetime(2020, 1, 1, tzinfo=dt_timezone.utc),
        end_dt=now_tz()
    )
    updated_at = LazyAttribute(lambda o: o.created_at + timedelta(hours=random.randint(0, 72)))
    moderated = FuzzyChoice([True, False])
