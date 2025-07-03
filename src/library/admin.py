from django.contrib import admin

from src.library.models import (
    Book,
    Post,
    # UserProfile,
    # Comment,
    Author,
    Category,
    Library,
    LibrariesMembers,
    Member
)

admin.site.register(Book)
admin.site.register(Post)
# admin.site.register(UserProfile)
# admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(Member)
admin.site.register(LibrariesMembers)