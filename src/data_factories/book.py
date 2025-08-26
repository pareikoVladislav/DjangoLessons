from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import List

import factory
from factory import LazyAttribute, Sequence
from factory import random as frandom
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyDecimal, FuzzyInteger
from factory.django import DjangoModelFactory

from django.utils import timezone

from src.data_factories.author import AuthorFactory
from src.data_factories.categories import CategoryFactory
from src.data_factories.libraries import LibraryFactory
from src.data_factories.users import UserFactory
from src.library.models import Book
from src.choices.base import Genre, Language


def choices_values(enum_cls) -> List[str]:
    # Получаем исходное представление choices у перечисления.
    raw = list(enum_cls.choices())
    # Если формат — пары (value, label), выбираем только value.
    if raw and isinstance(raw[0], (list, tuple)):
        return [c[0] for c in raw]
    # Иначе возвращаем как есть (уже список значений).
    return raw


GENRE_VALUES = choices_values(Genre)
LANG_VALUES = choices_values(Language)


def now_tz() -> datetime:
    return timezone.now()


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = Sequence(lambda n: f"Книга №{n}")
    description = factory.Faker("paragraph", nb_sentences=4, locale="en_US")
    genre = FuzzyChoice(GENRE_VALUES)
    pages = FuzzyInteger(50, 900)
    language = FuzzyChoice(LANG_VALUES)
    published_date = FuzzyDate(date(1990, 1, 1), date.today())
    publisher = factory.SubFactory(UserFactory)
    author = factory.SubFactory(AuthorFactory)
    category = factory.SubFactory(CategoryFactory)
    price = FuzzyDecimal(5.00, 200.00, precision=2)
    discounted_price = LazyAttribute(
        lambda o: (o.price * frandom.randgen.choice([
            Decimal("1.00"), Decimal("0.90"), Decimal("0.80")
        ])).quantize(Decimal("0.01"))
    )

    # Пост-обработчик для M2M-поля libraries: либо используем переданные, либо создаем 1-3 новых.
    @factory.post_generation
    def libraries(self, create, extracted, **kwargs):
        # Если объект не сохранён (build), связи не устанавливаем.
        if not create:
            return
        # Если библиотеки переданы извне — добавляем их как есть.
        if extracted:
            self.libraries.add(*extracted)
        # Иначе создаем случайное количество библиотек и связываем.
        else:
            libs = LibraryFactory.create_batch(frandom.randgen.randint(1, 3))
            self.libraries.add(*libs)

    # Набор трейтов для типовых сценариев цен/языков: позволяет быстро управлять параметрами нашей фабрики.
    class Params:
        # Принудительно английский язык.
        english_only = factory.Trait(language="en")
        # Дорогая книга с согласованной скидочной ценой.
        expensive = factory.Trait(price=Decimal("300.00"),
                                  discounted_price=Decimal("249.99"))
        # Бесплатная книга — обе цены равны нулю.
        free = factory.Trait(price=Decimal("0.00"),
                             discounted_price=Decimal("0.00"))
