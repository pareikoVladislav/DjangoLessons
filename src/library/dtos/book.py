from typing import Any

from rest_framework import serializers

from src.library.dtos.author import NestedAuthorShortInfoDTO
from src.library.dtos.library import NestedLibraryShortInfoDTO
from src.library.models import Book
from src.users.models import User


class BookListDTO(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'genre',
            'price',
            'language',
            'published_date',
            'author',
        )


class BookDetailedDTO(serializers.ModelSerializer):
    # published_date = serializers.DateField(
    #     write_only=True
    # )
    # price = serializers.DecimalField(
    #     max_digits=6,
    #     decimal_places=2,
    #     default=0.0,
    #     help_text="asdasdasdasd",
    #     write_only=True,
    #     required=False,
    #     allow_null=True,
    #     min_value=0.01,
    #     max_value=1000.00
    # )
    # author = NestedAuthorShortInfoDTO()
    # libraries = NestedLibraryShortInfoDTO(many=True)
    author = serializers.StringRelatedField()
    publisher = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )


    class Meta:
        model = Book
        fields = '__all__'


class BookCreateDTO(serializers.ModelSerializer):
    # discount_percent = serializers.DecimalField(
    #     max_digits=4,
    #     decimal_places=2,
    #     required=False,
    #     write_only=True,
    #     min_value=0,
    #     max_value=100
    # )

    class Meta:
        model = Book
        fields = (
            'title',
            'description',
            'genre',
            'pages',
            'language',
            'publisher',
            'discounted_price',
            # 'discount_percent',
            'author',
            'category',
            'price',
            'libraries'
        )

    # def validate_discounted_price(self, value: float) -> float:
    #     if not isinstance(value, (float, int)):
    #         raise serializers.ValidationError(
    #             "This field must be a float or number"
    #         )
    #
    #     return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        disc_price = attrs.get('discounted_price')
        price = attrs.get('price')

        if disc_price > price:
            raise serializers.ValidationError({
                "discounted_price": "Discounted price must be less than or equal to original price"
            })

        return attrs


    def create(self, validated_data: dict[str, Any]):
        from src.library.repositories.book import BookRepository

        book_repo = BookRepository()

        discount_percent = validated_data.pop('discount_percent', None)
        original_price = validated_data.get('price')


        if discount_percent and original_price:
            discount_amount = original_price * (discount_percent / 100)
            validated_data['discounted_price'] = original_price - discount_amount


        book = book_repo.create(**validated_data)

        return book
