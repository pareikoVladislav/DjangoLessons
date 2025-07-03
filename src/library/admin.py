from django.contrib import admin

from src.library.models import Book, Post, UserProfile, Comment, Author

admin.site.register(Book)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Author)
