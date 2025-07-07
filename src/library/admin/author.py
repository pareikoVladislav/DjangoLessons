from django.contrib import admin
from src.library.models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'profile']
    list_display = ('full_name', 'birth_date', 'rating', 'is_active')
    list_editable = ('rating', 'is_active')
    list_per_page = 15
    fieldsets = (
        (
            "Основная информация", {
                "fields": ("first_name", "last_name", "birth_date", )
            }
        ),
        (
            "Дополнительные данные", {
                "fields": ("profile", "is_active", "rating"),
                "classes": ("collapse",)
            }
        )
    )