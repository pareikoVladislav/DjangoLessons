from rest_framework import serializers

from src.library.models import Book


class BookListDTO(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'genre',
            'language',
            'published_date',
            'author',
        )


class BookDetailedDTO(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookCreateDTO(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'title',
            'description',
            'genre',
            'pages',
            'language',
            'publisher',
            'author',
            'category',
            'price'
        )
