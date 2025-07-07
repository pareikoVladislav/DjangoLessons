from django.contrib import admin
from django.utils.text import Truncator
from django.contrib import messages

from src.library.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'short_title',
        'author',
        'moderated',
        'created_at',
        'library__name',
    ]

    list_filter = [
        'moderated',
        'created_at',
        'author',
        'library__name'
    ]

    search_fields = [
        'title',
        'content',
        'author__last_name'
    ]

    list_per_page = 20

    fieldsets = (
        (
            'Content', {
                'fields': ('title', 'content', 'author')
            }
        ),
        (
            'Metadata', {
                'fields': ('moderated',)
            }
        ),
        (
            'Publication', {
                'fields': ('library',)
            }
        )
    )

    list_editable = ['moderated']

    list_select_related = ['library', 'author']

    @staticmethod
    def short_title(obj):
        return Truncator(obj.title).chars(50)

    actions = ['approve_moderation', 'moderated_to_csv']

    @admin.action(description='Approve moderation for selected posts')
    def approve_moderation(self, request, queryset):
        queryset.update(moderated=True)
        self.message_user(
            request,
            f"Selected posts are marked as moderated",
            messages.SUCCESS
        )

    @admin.action(description='Export moderated posts to CSV')
    def moderated_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        moderated_queryset = queryset.filter(moderated=True).select_related('author', 'library')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=moderated_posts.csv'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Moderated', 'Creation date', 'Library'])

        for post in moderated_queryset:
            writer.writerow(
                [
                    post.title,
                    f'{post.author.last_name} {post.author.first_name}',
                    post.moderated,
                    post.created_at,
                    post.library.name
                ]
            )

        return response