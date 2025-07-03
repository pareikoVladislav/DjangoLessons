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

admin.site.register(Book)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(Member)
admin.site.register(LibrariesMembers)
admin.site.register(Borrow)
admin.site.register(LibraryRecord)