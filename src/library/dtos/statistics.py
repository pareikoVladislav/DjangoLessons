import calendar

from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from src.library.dtos.book import BookListDTO


class BookCountPerLibraryDTO(serializers.Serializer):
    library = serializers.CharField()
    count_books = serializers.IntegerField()


class BookCountPerGenreDTO(serializers.Serializer):
    genre = serializers.CharField()
    count_books = serializers.IntegerField()


class BorrowCountPerGenreDTO(serializers.Serializer):
    genre = serializers.CharField()
    count_borrows = serializers.IntegerField()


class BorrowCountPerReaderDTO(serializers.Serializer):
    username = serializers.CharField()
    count_borrows = serializers.IntegerField()


class CountReadersPerLibraryDTO(serializers.Serializer):
    name = serializers.CharField()
    count_readers = serializers.IntegerField()


class TopWeekdayDTO(serializers.Serializer):
    weekday = serializers.SerializerMethodField()
    count_borrows = serializers.IntegerField()

    def get_weekday(self, obj):
        weekday_number = obj['weekday']
        return calendar.day_name[(weekday_number - 1)]


class LibraryStatisticDTO(serializers.Serializer):
    books_count = serializers.ListSerializer(child=BookCountPerLibraryDTO())
    most_popular_books = serializers.DictField()
    count_books_per_genre = serializers.DictField(
        child=serializers.ListSerializer(child=BookCountPerGenreDTO())
    )
    top_genres = serializers.DictField(
        child=serializers.ListSerializer(child=BorrowCountPerGenreDTO())
    )
    count_readers = serializers.ListSerializer(child=CountReadersPerLibraryDTO())
    top_readers = serializers.DictField(
        child=ListSerializer(child=BorrowCountPerReaderDTO())
    )
    top_active_weekdays = serializers.DictField(
        child=serializers.ListSerializer(child=TopWeekdayDTO())
    )

    def to_representation(self, instance):
        instance["most_popular_books"] = {
            library_id: BookListDTO(book_queryset, many=True).data
            for library_id, book_queryset in instance["most_popular_books"].items()
        }
        return super().to_representation(instance)
