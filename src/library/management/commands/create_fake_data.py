from __future__ import annotations

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from factory import random as factory_random

from src.data_factories import (
    CategoryFactory,
    LibraryFactory,
    UserFactory,
    AuthorFactory,
    BookFactory,
    LibraryRecordFactory,
    BorrowFactory,
    PostFactory
)


# Объявляем класс management-команды, чтобы её можно было запускать через manage.py.
class Command(BaseCommand):
    # Короткое описание, которое будет показано в подсказке по командам.
    help = "Заполняет БД реалистичными данными через Factory Boy"


    # Описываем CLI-аргументы команды, чтобы можно было конфигурировать объёмы данных и seed.
    def add_arguments(self, parser: CommandParser) -> None:
        # Строковый seed обеспечивает воспроизводимость генерации данных.
        parser.add_argument("--seed", type=str, default="demo-seed", help="Seed для воспроизводимости")
        # кол-во создаваемых категорий
        parser.add_argument("--categories", type=int, default=10)
        # кол-во библиотек
        parser.add_argument("--libraries", type=int, default=5)
        # Сколько пользователей создать
        parser.add_argument("--users", type=int, default=40)
        # Сколько авторов появится в системе.
        parser.add_argument("--authors", type=int, default=25)
        # Плановое число книг для генерации.
        parser.add_argument("--books", type=int, default=120)
        # Число новостей (постов) по библиотекам.
        parser.add_argument("--posts", type=int, default=40)
        # Сколько записей членства пользователей в библиотеках создать.
        parser.add_argument("--records", type=int, default=50)
        # Сколько выдач книг сгенерить.
        parser.add_argument("--borrows", type=int, default=150)


    # Делаем сидирование атомарной операцией, чтобы при ошибке не остались частично созданные данные.
    @transaction.atomic
    # Основная логика команды: читает параметры и создаёт данные в нужной последовательности.
    def handle(self, *args, **options):
        # Извлекаем seed из аргументов командной строки.
        seed: str = options["seed"]
        # Устанавливаем seed для фабрик и Faker -- синхронизирует источник случайности для повторяемых результатов.
        factory_random.reseed_random(seed)  # синхронизирует Faker и randomness фабрику
        # Сообщаем пользователю, с каким сидом выполняется генерация.(можно убрать, просто для наглядности)
        self.stdout.write(self.style.NOTICE(f"Seeding with seed={seed}"))


        # Блок 1: создаем справочники (категории и библиотеки) — они понадобятся остальным сущностям.
        # Генерируем пачку категорий в количестве, заданном параметром.
        CategoryFactory.create_batch(options["categories"])
        # Генерируем библиотеки — они будут использоваться далее для пользователей, постов и книг.
        libs = LibraryFactory.create_batch(options["libraries"])
        # Блок 2: создаем пользователей и авторов — ключевые субъекты домена.
        # Пользователи создаются батчем и сразу привязываются к первым двум библиотекам для M2M-связи.
        users = UserFactory.create_batch(options["users"], libraries=libs[:2])
        # Авторы создаются независимо от пользователей — их будет использовать BookFactory.
        AuthorFactory.create_batch(options["authors"])
        # Блок 3: генерируем книги с контролируемым распределением по «треитам» цен.
        # Идея: 70% — обычные, 20% — бесплатные, 10% — «дорогие»; так получаем разнообразный набор.
        books = []
        # Сколько книг нужно создать — читаем из аргументов.
        count = options["books"]
        # По количеству книг запускаем цикл создания.
        for i in range(count):
            # Текущий набор «трейтов» для фабрики книги.
            trait = None
            # Берём случайное число из RNG factory_boy, чтобы сохранять детерминизм с reseed_random.
            r = factory_random.randgen.random()
            # 10% книг — дорогие (expensive).
            if r < 0.1:
                trait = dict(expensive=True)
            # Следующие 20% — бесплатные (free).
            elif r < 0.3:
                trait = dict(free=True)
            # Остальные — базовая конфигурация без трейтов.
            else:
                trait = {}
            # Создаем книгу с выбранным набором трейтов и сохраняем ссылку для возможного последующего использования.
            b = BookFactory.create(**trait)
            # Кладем созданную книгу в общий список (например, для отладки/будущей логики).
            books.append(b)
        # Блок 4: создаём посты для случайных библиотек — эмулируем новостную активность.
        # Для заданного количества постов выбираем библиотеку случайно и создаем запись.
        for _ in range(options["posts"]):
            PostFactory.create(library=factory_random.randgen.choice(libs))
        # Блок 5: сначала генерируем записи членства, затем выдачи — это соблюдает целостность связей.
        # Накапливаем созданные записи членства, чтобы раздавать их в выдачах.
        records = []
        # Создаём записи членства, выбирая случайные пары пользователь/библиотека.
        for _ in range(options["records"]):
            rec = LibraryRecordFactory.create(
                member=factory_random.randgen.choice(users),
                library=factory_random.randgen.choice(libs),
            )
            # Добавляем запись в список для последующего использования.
            records.append(rec)
        # Создаём выдачи, каждый раз привязываясь к случайной записи членства.
        for _ in range(options["borrows"]):
            BorrowFactory.create(library_record=factory_random.randgen.choice(records))
        # Завершение работы команды — выводим сообщение об успешном сидировании.
        self.stdout.write(self.style.SUCCESS("Seeding completed"))


# python manage.py create_fake_data --seed=my-seed --categories=8 --libraries=4 --users=60 --authors=30 --books=150 --posts=60 --records=70 --borrows=220
