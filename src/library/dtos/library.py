from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from src.library.models import Library, LibraryRecord


class NestedLibraryShortInfoDTO(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = (
            'id',
            'name',
            'location'
        )


class LibraryCreateDTO(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"
        extra_kwargs = {
            'location': {'required': False},
        }


class LibraryRecordCreateDTO(serializers.ModelSerializer):
    class Meta:
        model = LibraryRecord
        fields = "__all__"
