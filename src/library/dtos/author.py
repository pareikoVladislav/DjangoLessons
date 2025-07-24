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
