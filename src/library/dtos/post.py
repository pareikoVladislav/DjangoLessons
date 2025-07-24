from rest_framework import serializers

from src.library.models import Post


class PostDTO(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('created_at', 'updated_at')
        extra_kwargs = {
            'moderated': {'required': False, 'default': False},
            'id': {'read_only': True, 'required': False},
        }
