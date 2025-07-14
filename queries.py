import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# ИМПОРТЫ НАШЕГО ФУНКЦИОНАЛА ДОЛЖНЫ БЫТЬ СТРОГО ПОСЛЕ СИСТЕМНОЙ НАСТРОЙКИ ВЫШЕ
from src.library.models import Book, Category, Author, Post, LibraryRecord, Borrow, Library
from src.users.models import User
from src.choices.base import Genre, Gender, Role
import datetime
from django.db.models.query import QuerySet
from django.db.models import Q, F


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


# user = User(
#     username='Biba',
#     email='Biba@test.com',
#     role= Role.reader,
#     first_name='Biba',
#     last_name='Bobov',
#     gender= Gender.male,
#     age=25,
# )
#
# user.set_password('qwerty1234')
# user.save()

# User.objects.filter(first_name="Biba").delete()

"""
## Задача 5: Поиск авторов с использованием field lookups
**ТЗ:**
1. Найти всех авторов, чье имя начинается с 'A'
2. Найти авторов с рейтингом выше 8.5
3. Найти авторов, родившихся после 1950 года
4. Получить первого автора из результата
"""

# a_authors = Author.objects.filter(first_name__startswith='A')
#
# print(a_authors)
#
# graded_author = Author.objects.filter(rating__gt=8.5)
#
# print(graded_author)
#
# born_authors = Author.objects.filter(birth_date__gt=datetime.date(1950, 1, 1)).first()
#
# print(born_authors)

"""
## Задача 10: Сложные фильтры с Q-объектами
**ТЗ:**
1. Найти авторов, которые либо имеют рейтинг выше 9.0, либо родились до 1900 года
2. Среди найденных авторов взять только активных
3. Исключить авторов без указанной даты рождения
4. Подсчитать общее количество и проверить существование
"""

"""Задача 14: Создание записей займов с валидацией
**ТЗ:**
1. Найти LibraryRecord с id=5
2. Найти книгу с id=25
3. Создать новый заем (Borrow) с датой займа сегодня и датой возврата через 30 дней
4. Проверить, что запись была создана и получить ее id
"""

# library_records = LibraryRecord.objects.filter(id=5)
# book = Book.objects.get(id=25)
#
# borrow = Borrow.objects.create(
#     return_date = timezone.now() + timedelta(days=30),
#     book = book,
#     library_record = library_records[0],
# )

"""
## Задача 15: Поиск библиотек с фильтрацией по местоположению
**ТЗ:**
1. Найти все библиотеки, в названии которых есть слово "Central" (регистронезависимо)
2. Найти библиотеки, расположенные в городах, содержащих "New" в названии
3. Объединить результаты с помощью Q-объектов
4. Исключить библиотеки без веб-сайта
"""
#
# library_central = Library.objects.filter(name__icontains='Central')
#
# library_new_loc = Library.objects.filter(location__contains='New')
#
# library_combo = Library.objects.filter(Q(name__icontains='Central') | Q(name__icontains='New'))
#
# libs_wo_ws = Library.objects.exclude(website__isnull=True)
#
# print(library_central)
# print(library_new_loc)
# print(library_combo)
# print(libs_wo_ws)

"""
## Задача 16: Сложная фильтрация авторов по активности и рейтингу
**ТЗ:**
1. Найти активных авторов с рейтингом от 8.0 до 9.5 включительно
2. Среди них найти тех, кто родился в XX веке (1901-2000 годы)
3. Исключить авторов без указанной даты рождения
4. Получить только первые 10 результатов
"""

# authors = Author.objects.filter(
#     is_active=True,
#     rating__gte=8,
#     rating__lte=9.5,
#     birth_date__year__gte=1901,
#     birth_date__year__lte=2000,
# )[:10]
#
# print(authors)

"""
## Задача 20: Сложный поиск займов с временными условиями
**ТЗ:**
1. Найти все займы, сделанные в 2022 году
2. Среди них найти те, которые были возвращены вовремя (до или в дату return_date)
3. Исключить займы без указанной даты возврата
4. Сгруппировать результаты по месяцам и посчитать количество в каждом месяце
"""

# sorted_borrows = Borrow.objects.filter(
#     borrow_date__year=2022,
#     is_overdue=False,
#     return_date__isnull=False,
# )

# borrows = Borrow.objects.filter(
#     borrow_date__year=2022,
#     return_date__lt=now(),
#     is_returned=False
# ).exclude(return_date__isnull=True)
#
# count_borrows = Counter([borrow.borrow_date.month for borrow in borrows])
#
# print(count_borrows)

