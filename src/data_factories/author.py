from __future__ import annotations

from datetime import date

import factory
from factory.fuzzy import FuzzyDate, FuzzyFloat
from factory.django import DjangoModelFactory

from src.library.models import Author


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker("first_name", locale="en_US")
    last_name  = factory.Faker("last_name",  locale="en_US")
    birth_date = FuzzyDate(date(1940, 1, 1), date(2000, 12, 31))
    profile = factory.Maybe("has_profile", yes_declaration=factory.Faker("url"), no_declaration=None)
    is_active = True
    rating = FuzzyFloat(1.0, 10.0)
    deleted = False
    deleted_at = None

    class Params:
        # По умолчанию у автора есть профиль.
        has_profile = True
        # Трейт для неактивного автора.
        inactive = factory.Trait(is_active=False)
