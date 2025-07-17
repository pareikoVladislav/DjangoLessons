from rest_framework import serializers

from src.library.models import Library


class NestedLibraryShortInfoDTO(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = (
            'id',
            'name',
            'location'
        )
