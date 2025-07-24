from rest_framework import serializers

from src.library.models import Borrow


class BorrowDTO(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = "__all__"


class OverdueBorrowsDTO(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title")
    member = serializers.CharField(source="library_record.member")

    class Meta:
        model = Borrow
        fields = (
            "id",
            "book_title",
            "borrow_date",
            "return_date",
            "is_returned",
            "member"
        )
