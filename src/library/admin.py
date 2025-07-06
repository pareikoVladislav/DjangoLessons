from django.contrib import admin

from src.library.models import (
    Book,
    Post,
    Author,
    Category,
    Library,
    LibrariesMembers,
    Member,
    Borrow,
    LibraryRecord
)

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


# admin.site.register(Book, BookAdmin)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(Member)
admin.site.register(LibrariesMembers)
admin.site.register(Borrow)
admin.site.register(LibraryRecord)