from rest_framework import serializers

from src.users.models import User


class ListUsersDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'books'
        )

    def to_representation(self, instance):
        basic_repr = super().to_representation(instance)
        if self.context.get('include_related'):
            basic_repr['books'] = [
                {
                    "id": b.id,
                    "title": b.title,
                    "genre": b.genre,
                    "language": b.language,
                    "category": b.category.title,
                    "price": b.price,
                }
                for b in instance.books.all()
            ]

        return basic_repr


class DetailedUserDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_active",
            "is_staff",
            "date_joined",
            "groups",
            "user_permissions"
        )


class CreateUserDTO(serializers.ModelSerializer):
    repeat_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password',
            'repeat_password',
            'role',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs: dict) -> dict:
        password = attrs.get('password')
        repeat_password = attrs.pop('repeat_password')

        if password != repeat_password:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })

        return attrs

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)

        return user
