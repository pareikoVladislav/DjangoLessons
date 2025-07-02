from django.contrib import admin

from src.library.models import Book, Post, UserProfile, Comment


admin.site.register(Book)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
