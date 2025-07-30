from rest_framework import serializers

from src.library.models import Author


class NestedAuthorShortInfoDTO(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'last_name',
            'rating',
        )


class AuthorDTO(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorCreateUpdateDTO(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'profile',
            'rating',
        ]
        extra_kwargs = {
            'rating': {'required': False},
            'profile': {'required': False},
            'birth_date': {'required': False},
        }