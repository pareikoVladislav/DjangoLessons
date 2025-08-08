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
    def to_representation(self, instance):
        resp = super().to_representation(instance)
        if self.context.get('include_related'):
            if instance.author:
                resp['author'] = {
                    'id': instance.author.id,
                    'name': f"{instance.author.last_name} {instance.author.first_name[0]}."
                }
            else:
                resp['author'] = None
            resp['category'] = (
                instance.category.title if instance.category else None
            )
        return resp

class BookDetailedDTO(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    publisher = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )


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
            'price',
            'libraries'
        )

        extra_kwargs = {
            'publisher': {'required': False},
        }

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        disc_price = attrs.get('discounted_price')
        price = attrs.get('price')

        if disc_price and disc_price > price:
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
