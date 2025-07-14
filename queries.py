import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# ИМПОРТЫ НАШЕГО ФУНКЦИОНАЛА ДОЛЖНЫ БЫТЬ СТРОГО ПОСЛЕ СИСТЕМНОЙ НАСТРОЙКИ ВЫШЕ
from src.library.models import Book, Category, Author, Post, Borrow, book
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

sub_query = Book.objects.filter(
    author=OuterRef('author')).values('author').annotate(
    min_price=Min('price')
).values('min_price') # U0


primary_query = Book.objects.annotate( # Book.objects.all() => SELECT *
    min_price=Subquery(
        sub_query,
        output_field=DecimalField(max_digits=6, decimal_places=2)
    )
)

print(primary_query.query)


for obj in primary_query:
    print(obj)
