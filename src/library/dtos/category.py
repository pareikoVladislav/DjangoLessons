from rest_framework import serializers

from src.library.models import Category

class CategoryDTO(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
