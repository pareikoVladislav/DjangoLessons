from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from src.library.models import Library


class LibraryFactory(DjangoModelFactory):
    class Meta:
        model = Library

    name = factory.Faker("company", locale="en_EN")
    location = factory.Faker("address", locale="en_EN")
    website = factory.Maybe(
        "has_site",
        yes_declaration=factory.Faker("url", locale="en_EN"),
        no_declaration=None,
    )

    class Params:
        has_site = True
