from django.contrib import admin
from src.library.models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'profile']
    list_display = ('full_name', 'birth_date', 'age_display', 'count_books_display','rating', 'is_active')
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
    actions = ['deactivate_authors', 'activate_authors', 'export_to_json']

    @admin.action(description="Деактивировать выбранных авторов")
    def deactivate_authors(self, request, queryset):
        queryset.update(is_active=False)
        return request

    @admin.action(description="Активировать выбранных авторов")
    def activate_authors(self, request, queryset):
        queryset.update(is_active=True)
        return request

    @admin.action(description="Экспорт в JSON")
    def export_to_json(self, request, queryset):
        import json
        from django.http import HttpResponse

        data = list(queryset.values())
        for item in data:
            for key, value in item.items():
                if hasattr(value, 'isoformat'):
                    item[key] = value.isoformat()
        file_data = json.dumps(data)
        response = HttpResponse(file_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=author.json'
        return response

    @admin.display(description="Возраст")
    def age_display(self, obj):
        from django.utils import timezone
        if obj.birth_date:
            today = timezone.now().date()
            age = today.year - obj.birth_date.year
            if (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day):
                age -= 1
            return age
        return 0

    @admin.display(description="Колл-во книг")
    def count_books_display(self, obj):
        return obj.books.count()