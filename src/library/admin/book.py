from django.contrib import admin

from src.library.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'genre',
        'pages',
        'language',
        'published_date',
        'category'
    ]

    search_fields = [
        'title',
        'genre',
        'category__title',
        'publisher__last_name'
    ]

    list_filter = [
        'genre',
        'published_date',
        'language'
    ]

    list_editable = ['genre', 'language']

    list_per_page = 10
    # list_max_show_all = 25

    list_select_related = ['category',]

    fieldsets = (
        (
            "Basic Information", {
            "fields": ("title", "description", "genre")
        }
        ),
        (
            "Publication Details", {
            "fields": ("publisher", "pages", "language"),
            "classes": ("collapse", )
        }
        ),
        (
            "Classification", {
            "fields": ("category", "libraries"),
            "classes": ("collapse", )
        }
        ),
    )

    actions = ['export_to_csv', 'set_genre_to_fiction']


    @admin.action(description="Export selected books to CSV")
    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=data.csv'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Genre', 'Pages', 'Language', 'Published Date', 'Category'])

        for book in queryset:
            writer.writerow([
                book.title, book.genre or 'N/A', book.pages or 0, book.language, book.published_date, book.category.title
            ])

        return response

    @admin.action(description="Set genre to fiction")
    def set_genre_to_fiction(self, request, queryset):
        for obj in queryset:
            obj.genre = 'FICTION'
            obj.save()

        return request



