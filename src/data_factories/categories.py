from __future__ import annotations

import factory
from factory import Sequence
from factory.django import DjangoModelFactory

from src.library.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('title',)

    # title = Sequence(lambda index: f"Category {index:03d}")
    title = factory.Faker('word', locale='en_US')
    # Category 001
    # Category 002
    # Category 003
    # Category 004
