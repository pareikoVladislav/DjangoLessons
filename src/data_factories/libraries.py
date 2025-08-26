from __future__ import annotations

import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from src.library.models import Library


class LibraryFactory(DjangoModelFactory):
    class Meta:
        model = Library

    name = factory.Faker("company", locale="en_US")
    location = factory.Faker("address", locale="en_US")
    website = factory.Maybe(
        "has_site",
        yes_declaration=factory.Faker("url", locale="en_US"),
        no_declaration=None,
    )

    class Params:
        has_site = FuzzyChoice([True, False, False])  # Будет примерно 33 процента на True
