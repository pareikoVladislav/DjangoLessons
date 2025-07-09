import os


import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# ИМПОРТЫ НАШЕГО ФУНКЦИОНАЛА ДОЛЖНЫ БЫТЬ СТРОГО ПОСЛЕ СИСТЕМНОЙ НАСТРОЙКИ ВЫШЕ
from src.library.models import Book, Category, Author, Post, Borrow, LibraryRecord, Library
from src.users.models import User
from src.choices.base import Genre, Gender, Language, Role
from collections import Counter

from django.db.models.query import QuerySet
from django.db.models import Q, F
from datetime import timedelta, date, datetime
from django.utils.timezone import now


# books = Book.objects.all()
#
#
# print(books)
# print(books[0].title)


# pub = User.objects.get(username='ich1')
# author = Author.objects.get(last_name='Sapkowski')
# cat = Category.objects.get(pk=4)

# new_book = Book(
#     title='Test Book from ORM system',
#     genre=Genre.FANTASY,
#     pages=215,
#     publisher=pub,
#     author=author,
#     category=cat,
# )
#
# new_book.save()

# print(new_book)
# print(new_book.title)
# print(new_book.genre)
# print(new_book.publisher)
# print(new_book.author)
# print(new_book.category)


# pub = User.objects.get(username='ich1')
# author = Author.objects.get(last_name='Sapkowski')
# cat = Category.objects.get(pk=5)
#
# new_book = Book.objects.create(
#     title='NEW BOOK',
#     genre=Genre.BIOGRAPHY,
#     pages=400,
#     publisher=pub,
#     author=author,
#     category=cat,
# )
#
# print(new_book)
# print(new_book.genre)
# print(new_book.publisher)
# print(new_book.author)
# print(new_book.category)


# books: QuerySet = Book.objects.all()
#
# print(type(books))
# print(books)
#
# print(books.query)
#
# for i in range(5):
#     print(books[i].title)

# first_book: Book = Book.objects.first()
#
# print(first_book)


# last_book: Book = Book.objects.last() # The Witcher: The Last Wish
#
# print(last_book)

# latest_book: Book = Book.objects.latest() # The Witcher: The Last Wish
#
# print(latest_book)


# books_count = Book.objects.count()
#
# print(f"Кол-во книг в базе = {books_count}")




# books_exists: bool = Book.objects.all().exists()
#
# print(f"Набор данных наполнен - {books_exists}")

#
# books: QuerySet = Book.objects.values(
#     'title',
#     'genre',
#     'published_date',
#     'language'
# )
#
#
# print(books.query)
#
# for i in range(10):
#     print(
#         books[i]['title'],
#         books[i]['genre'],
#         books[i]['published_date'],
#         books[i]['language']
#     )

# filtered_books: QuerySet = Book.objects.filter(
#     genre='BIOGRAPHY',
#     publisher_id=2
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     genre__in=[Genre.FANTASY, Genre.BIOGRAPHY],
#     publisher_id__in=[17, 25, 35, 43, 50, 20]
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     title__iexact='the' # the The THE
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     title__istartswith='the' # the The THE
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     title__icontains='the' # the The THE
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     pages__gt=250,
#     pages__lte=500
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     published_date__gt="2023-04-01"
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     description__isnull=True
# )
#
# print(filtered_books.query)
# print(filtered_books)


# filtered_books: QuerySet = Book.objects.filter(
#     published_date__range=["2023-01-01", "2023-12-31"]
# )
#
# print(filtered_books.query)
# print(filtered_books.count())



# filtered_books: QuerySet = Book.objects.filter(
#     description__isnull=True,
#     category_id=5
# )
#
# print(filtered_books.query)
# print(filtered_books.count())

# filtered_books: QuerySet = Book.objects.filter(
#     Q(description__isnull=True) & ~Q(category_id=5)
# )
#
# print(filtered_books.query)
# print(filtered_books)



# filtered_books: QuerySet = Post.objects.filter(
#     ~Q(moderated=True) | (Q(title__istartswith='F') & Q(author_id=21))
# )
#
# print(filtered_books.query)
# print(filtered_books)



# req_author: Author = Author.objects.get(
#     last_name='Sapkowski',
#     first_name='Andrzej'
# )
#
# print(req_author)
#
# print(req_author.rating)
#
#
# req_author.rating = 9.5
#
# req_author.save()


# req_authors = Author.objects.filter(
#     rating__lt=8
# )
#
# req_authors.update(rating=8.2)  # UPDATE table SET rating=8.2 WHERE rating < 8;
#
# req_authors.update()


# req_authors = Author.objects.filter(
#     rating__lt=8.5
# )
#
# print(req_authors.query)
#
# req_authors.update(rating=F('rating') * 0.90)  # UPDATE table SET rating=8.2 WHERE rating < 8;
#
# req_authors.update(discounted_price=F('price') * 0.85)
#
#
# Book.objects.filter(
#     discounted_price__lt=F('price')
# )


# req_obj = Book.objects.get(title='Test Book from ORM system')
#
# print(type(req_obj))
#
# deleted_obj = req_obj.delete()
#
# req_obj.save()

# user = User.objects.create(
#     username="new_user",
#     first_name="John",
#     last_name="Doe",
#     email="new_user@test.com",
#     gender=Gender.male,
#     role="reader",
#     age=25,
# )
#
# user.set_password("My_pass999")
# print(user)

# books = Book.objects.filter(
#     genre=Genre.FICTION,
#     language=Language.en.name
# )
#
# if books.exists():
#     print(books)
#     print(books.count())
#
# else:
#     print("Nothing founded")


# users = User.objects.filter(
#     Q(role=Role.admin.value) | Q(role=Role.employee.value)
# )
#
# users.exclude(is_active=False)
# users.order_by('-date_joined')
#
# for user in users[:4]:
#     print(user.date_joined)


# authors_A = Author.objects.filter(
#     first_name__startswith="A",
# )
# print(authors_A)
# top_authors = Author.objects.filter(
#     rating__gt=8.5
# )
# print(top_authors)
# new_authors = Author.objects.filter(
#     birth_date__year__gt=1950
# )
#
# print(new_authors)
#
# print(new_authors.first())


# authors = Author.objects.filter(
#     Q(rating__gt=9) | Q(birth_date__year__lt=1900),
#     is_active=True
# )
# print(authors)
# authors_with_b_date = (authors.exclude(
#     birth_date__isnull=True
# ))
# print(authors_with_b_date)
# print(authors_with_b_date.count())
# print(authors_with_b_date.exists())

# library_record= LibraryRecord.objects.get(id=5)
# book = Book.objects.get(id=25)
#
# borrow = Borrow.objects.create(
#     return_date=now() + timedelta(days=30),
#     book=book,
#     library_record=library_record
# )
#
# print(borrow.id)

# libraries = Library.objects.filter(
#     Q(name_icontains="Central") & Q(name_icontains="Central")
# )
#
# libraries.exclude(website__isnull=True)

#
# authors = Author.objects.filter(
#     is_active=True,
#     rating__range=(8, 9.5),
#     birth_date__range=(date(1901, 1, 1), date(2000, 1, 1))
# )
#
# res = authors.exclude(birth_date__isnull=True)[:10]


# exist_category = Category.objects.filter(title="Фантастика").exists()
#
# category = Category.objects.get_or_create(title="Фантастика")
# books_count = Book.objects.filter(category__title="Фантастика").count()
# print(f"В категории {category[0].title} {books_count} книг")


# users = User.objects.filter(
#     role=Role.reader
# )
# library = Library.objects.get(pk=9)
#
# library_records = [
#     LibraryRecord(user=user, library=library)
#     for user in users
# ]
#
# LibraryRecord.objects.bulk_create(library_records)

# borrows = Borrow.objects.filter(
#     borrow_date__year=2022,
#     return_date__lt=now(),
#     is_returned=False
# ).exclude(return_date__isnull=True)
#
# count_borrows = Counter([borrow.borrow_date.month for borrow in borrows])
#
# print(count_borrows)

# ## Задача 22: Создание постов с валидацией и связями
# **ТЗ:**
# 1. Найти активного автора с наивысшим рейтингом
# 2. Создать для него 3 поста с разными заголовками
# 3. Проверить, что все посты были созданы успешно
# ## Задача 23: Сложная фильтрация займов по датам и статусам

most_popular = Author.objects.all().order_by("-rating").first()

Post.objects.bulk_create(
    Post(
        title="Some title",
        content="Some content",
        author=most_popular,
        library=...
    ),
    Post(
        title="Some title1",
        content="Some content1",
        author=most_popular,
    ),
    Post(
        title="Some title2",
        content="Some content2",
        author=most_popular,
    ),
)
# **ТЗ:**
# 1. Найти займы, сделанные в последние 6 месяцев от текущей даты
# 2. Среди них найти те, которые должны были быть возвращены более 30 дней назад
# 3. Исключить уже возвращенные займы
# 4. Получить информацию о библиотеке и пользователе для каждого займа
# ## Задача 24: Массовое обновление авторов с условной логикой
# **ТЗ:**
# 1. Найти всех авторов без указанной даты рождения
# 2. Найти авторов с рейтингом ниже 5.0
# 3. Объединить эти группы с помощью Q-объектов
# 4. Массово установить им рейтинг 5.0 и статус is_active=False
# ## Задача 25: Поиск пользователей по активности в библиотеках
# **ТЗ:**
# 1. Найти всех пользователей, которые связаны с более чем одной библиотекой
# 2. Среди них найти тех, кто имеет активные займы (не возвращенные)
# 3. Исключить пользователей с ролью 'admin'
# 4. Отсортировать по дате регистрации
# ## Задача 26: Создание связей между книгами и библиотеками
# **ТЗ:**
# 1. Найти все книги жанра 'SCIENCE_FICTION'
# 2. Найти библиотеки, в названии которых есть слово "Tech"
# 3. Создать связи many-to-many между этими книгами и библиотеками
# 4. Проверить, что связи были созданы
# ## Задача 27: Анализ займов по временным периодам
# **ТЗ:**
# 1. Найти все займы за 2023 год
# 2. Разделить их на кварталы (Q1: янв-март, Q2: апр-июнь, Q3: июль-сен, Q4: окт-дек)
# 3. Для каждого квартала посчитать количество займов и возвратов
# 4. Найти квартал с наибольшей активностью
# ## Задача 28: Поиск и создание категорий с иерархией
# **ТЗ:**
# 1. Проверить существование категорий: "Классическая литература", "Современная проза", "Детская литература"
# 2. Создать отсутствующие категории
# 3. Найти книги без категории и присвоить им категорию "Без категории"
# 4. Вывести статистику по количеству книг в каждой категории
# ## Задача 29: Сложный поиск с множественными связями
# **ТЗ:**
# 1. Найти пользователей, которые зарегистрированы в библиотеках с веб-сайтом
# 2. Среди них найти тех, кто брал книги автора с рейтингом выше 8.0
# 3. Исключить пользователей младше 21 года
# 4. Получить уникальный список таких пользователей
# ## Задача 30: Комплексная работа с датами и статусами
# **ТЗ:**
# 1. Найти все займы, которые были сделаны в выходные дни (суббота/воскресенье)
# 2. Среди них найти те, которые длились более 45 дней
# 3. Проверить статус возврата и подсчитать просроченные
# 4. Создать отчет по библиотекам с наибольшим количеством проблемных займов

