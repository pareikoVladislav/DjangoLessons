from __future__ import annotations

import random
from datetime import date, timedelta

import factory
from factory import LazyAttribute
from factory.fuzzy import FuzzyChoice
from factory.django import DjangoModelFactory

from src.data_factories.book import BookFactory
from src.data_factories.libraries import LibraryFactory
from src.data_factories.users import UserFactory
from src.library.models import LibraryRecord, Borrow, Book


class LibraryRecordFactory(DjangoModelFactory):
    class Meta:
        model = LibraryRecord

    member = factory.SubFactory(UserFactory)
    library = factory.SubFactory(LibraryFactory)


class BorrowFactory(DjangoModelFactory):
    class Meta:
        model = Borrow

    library_record = factory.SubFactory(LibraryRecordFactory)
    borrow_date = LazyAttribute(lambda _: date.today())
    return_date = LazyAttribute(lambda o: o.borrow_date + timedelta(days=random.randint(7, 30)))
    is_returned = FuzzyChoice([True, False, False])  # чаще невозвращенные

    # Книга должна быть доступна хотя бы в библиотеке library_record.library
    # Вычисляем книгу динамически: либо берем имеющуюся в библиотеке, либо создаем новую и привязываем.
    @factory.lazy_attribute
    def book(self):
        # Получаем библиотеку из записи членства — контекст для поиска книги.
        lib = self.library_record.library
        # Пытаемся найти существующие книги, связанные с этой библиотекой через M2M.
        # попробуем выбрать существующую книгу из этой библиотеки
        book_qs = Book.objects.filter(libraries=lib)
        # Если книги есть — возвращаем случайную из небольшого среза(можно и все оставить, но так будет больше места в памяти занимать)
        if book_qs.exists():
            return random.choice(list(book_qs[:50]))
        # В противном случае создаем новую книгу и тут же привязываем к библиотеке.
        book = BookFactory.create(libraries=[lib])

        # Возвращаем выбранную/созданную книгу.
        return book
