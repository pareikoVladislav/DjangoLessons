from django.contrib import admin

from src.library.models import *
from src.library.admin.book import BookAdmin
from src.library.admin.borrow import BorrowAdmin


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(LibrariesMembers)
#admin.site.register(Borrow)
admin.site.register(LibraryRecord)