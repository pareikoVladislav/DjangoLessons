import os
import django

from src.choices.base import Genre, Role

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# ИМПОРТЫ НАШЕГО ФУНКЦИОНАЛА ДОЛЖНЫ БЫТЬ СТРОГО ПОСЛЕ СИСТЕМНОЙ НАСТРОЙКИ ВЫШЕ
from src.library.models import Book, Category, Author, Post, Borrow, book
from src.users.models import User

import datetime
from django.db.models.query import QuerySet
from django.db.models import Q, F, Avg, Count, Min, Max, Sum


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



# добавить + 1 новое поле на дату возврата borrow (а то пока непонятно когда книга быа возвращена)


# last_borrow = Borrow.objects.last()
#
#
# print(last_borrow)
#
# print(last_borrow.is_overdue)


# aggregate()

from django.db.models import Avg, Min, Max, Count, Sum


# aggregate_data = Book.objects.aggregate(
#     total_books=Count('id'),
#     avg_cost=Avg('price')
# )
#
# print(aggregate_data)
# print(f"Общее кол-во книг: {aggregate_data['total_books']}")
# print(f"Средняя цена всех книг: {aggregate_data['avg_cost']}")


# total_books_cost = Book.objects.aggregate(
#     total_cost=Sum('price')
# )
#
# print(f"Общая цена всех книг: {total_books_cost['total_cost']}")


# books_count_by_author = Book.objects.values('author').annotate(
#     books_count=Count('id')
# )[10:20]
#
# print(books_count_by_author.query)
#
#
# for obj in books_count_by_author:
#     print(f"Автор : {obj['author']}, Количество его книг = {obj['books_count']}")



# Получение книг с ценой выше средней


# avg_price = Book.objects.aggregate(
#     avg_price=Avg('price')
# )['avg_price']
#
#
# prim_query = Book.objects.filter(
#     price__gt=avg_price
# ).values('title', 'price', 'author')[:7]
#
#
# print(prim_query.query)
# print(prim_query)
#
# for obj in prim_query:
#     print(f"{obj['title']}   ---   {obj['price']}   ---   {obj['author']}")


# avg_price = Book.objects.aggregate(
#     avg_price=Avg('price')
# )
#
# # print(avg_price.query)
# print(avg_price)


from django.db.models import OuterRef, Subquery, DecimalField

# sub_query = Book.objects.filter(
#     author=OuterRef('author')).values('author').annotate(
#     min_price=Min('price')
# ).values('min_price') # U0
#
#
# primary_query = Book.objects.annotate( # Book.objects.all() => SELECT *
#     min_price=Subquery(
#         sub_query,
#         output_field=DecimalField(max_digits=6, decimal_places=2)
#     )
# )
#
# print(primary_query.query)
#
#
# for obj in primary_query:
#     print(obj)

#
# from django.db.models import Case, When, F
#
# authors_problematic_query = Author.objects.annotate(
#     performance_score=Case(
#         When(books__price__gt=100, then=F('books__price') * 2),
#         When(books__price__gt=50, then=F('books__price') * 1.5),
#         default=F('books__price')
#     )
# )
#
# print(authors_problematic_query.query)
#
#
# for a in authors_problematic_query[:3]:
#     print(f"Автор: {a.first_name} {a.last_name}")
#     print(f"Рейтинг производительности автора: {a.performance_score}")
#     print(f"Тип результата: {type(a.performance_score)}")


# from decimal import Decimal
#
#
# a = Decimal('22.17')
#
# b = 3.14
#
# print(a * b)



# from django.db.models import Case, When, F, ExpressionWrapper, Value
#
# authors_problematic_query = Author.objects.annotate(
#     performance_score=Case(
#         When(
#             books__price__gt=100,
#             then=ExpressionWrapper(F('books__price') * 2.0,
#                                    output_field=DecimalField())
#         ),
#         When(
#             books__price__gt=50,
#             then=ExpressionWrapper(
#                 F('books__price') * 1.5,
#                 output_field=DecimalField()
#             )
#         ),
#         default=F('books__price')
#     )
# )
#
# print(authors_problematic_query.query)
#
#
# for a in authors_problematic_query[:3]:
#     print(f"Автор: {a.first_name} {a.last_name}")
#     print(f"Рейтинг производительности автора: {a.performance_score}")
#     print(f"Тип результата: {type(a.performance_score)}")


# from rest_framework import serializers
#
#
# class CustomSerializerClass(serializers.Serializer):
#     name = serializers.CharField(max_length=30)
#     age = serializers.IntegerField(min_value=0)
#     is_active = serializers.BooleanField()
#     created_at = serializers.DateTimeField()
#
#
#
# data = CustomSerializerClass(
#     data={
#         'name': 'John',
#         'age': 2,
#         'is_active': True,
#         'created_at': '2021-01-01T00:00:00Z'
#     }
# )
#
# print(data)
# print(data.initial_data)
#
# if data.is_valid():
#     print(data.validated_data)
#
# else:
#     print(data.errors)


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('title',)
#
#
# new_category = CategorySerializer(
#     data={
#         "title": "+" * 35
#     }
# )
#
# print(new_category)
#
# try:
#     new_category.is_valid(raise_exception=True)
#
#     print("DATA IS VALID!!!!")
#     print(new_category.validated_data)
# except serializers.ValidationError as e:
#     print(e)


# ### **Задача 1: Общее количество книг и их средняя цена**
# **ТЗ:** Получить общее количество книг в базе данных и среднюю цену всех книг в одном запросе

# result = Book.objects.aggregate(
#     total=Count('id'),
#     avg_price=Avg('price')
# )
#
# print(result)


### **Задача 2: Диапазон цен и общее количество страниц**
# **ТЗ:** Найти минимальную, максимальную цену книг и общее количество страниц всех книг
#
# result = Book.objects.aggregate(
#     min_price=Min('price'),
#     max_price=Max('price'),
#     total_pages=Sum('pages')
# )
# print(result)

### **Задача 3: Количество книг по каждому жанру**
# **ТЗ:** Подсчитать количество книг в каждом жанре, отсортировать по убыванию количества

# result = Book.objects.values('genre').annotate(
#     book_count=Count('id')
# ).order_by('-book_count')
#
# for genre in result:
#     print(f'{genre['genre']} : {genre['book_count']}')

### **Задача 4: Средняя цена книг по каждому языку**
# **ТЗ:** Вычислить среднюю цену книг для каждого языка и количество книг на каждом языке

# result = Book.objects.values('language').annotate(
#     avg_price=Avg('price'),
#     book_count=Count('id')
# ).order_by('-avg_price')
#
# for lang in result:
#     print(f"Language: {lang['language']}, Average Price: {lang['avg_price']}, Book Count: {lang['book_count']}")
#
#
# ### **Задача 5: Авторы с количеством книг и средним рейтингом**
# # **ТЗ:** Получить всех авторов с количеством написанных книг, отсортировать по убыванию количества книг
#
# author_rated_books_amount = Author.objects.annotate(
#     book_count=Count('books'),
#     avg_rating=Avg('rating'),
#
# ).order_by('-book_count')
#
# for author in author_rated_books_amount:
#     print(f"Author: {author.first_name} {author.last_name}", f"Book Count: {author.book_count}", f"Average Rating: {author.avg_rating}")
#
# ### **Задача 6: Топ-5 читателей по количеству активных займов**
# # **ТЗ:** Найти 5 пользователей с наибольшим количеством невозвращенных книг
#
# top_borrowers = User.objects.filter(
#     role=Role.reader).annotate(
#     active_borrows=Count('borrows__borrows', filter=Q(borrows__borrows__is_returned=False)),
#
#
# ).filter(active_borrows__gt=0).order_by('-active_borrows')[:5]
#
# print("Top 5 Borrowers:")
# for user in top_borrowers:
#     print(f"{user.first_name} {user.last_name} ({user.username}) - {user.active_borrows} active borrow(s)")

# import locale
# import calendar
#
#
# try:
#     locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# except locale.Error:
#     pass
#
#
# def get_month_names_mapping():
#     return {
#         i: calendar.month_name[i]
#         for i in range(1, 13)
#     }
# def get_month_abbr_names_mapping():
#     return {
#         i: calendar.month_abbr[i]
#         for i in range(1, 13)
#     }
#
#
# def get_weekday_names_mapping():
#     return {
#         i: calendar.day_name[i-1]
#         for i in range(1, 8)
#     }
#
# print(get_month_names_mapping())
# print(get_month_abbr_names_mapping())
# print(get_weekday_names_mapping())
# from django.db.models.functions import ExtractMonth
# from django.db.models import Count, Case, When, CharField, Value
# from django.utils.translation import gettext_lazy as _
#
#
# def generate_cases():
#     month_names = get_month_names_mapping()
#
#     cases = [
#         When(pub_month_num=num, then=_(name))
#         for num, name in month_names.items()
#     ]
#
#     return Case(*cases, output_field=CharField())
# books_with_month_names = Book.objects.annotate(
#     pub_month_num=ExtractMonth('published_date'),
#     pub_month_name=generate_cases()
# ).values('pub_month_name').annotate(
#     count_ob_books=Count('id')
# )
#
# print(books_with_month_names)

# b = Book.objects.all().explain(analyze=True)
#
# print(b)