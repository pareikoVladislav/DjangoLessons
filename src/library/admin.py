from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from src.library.models import (
    Book,
    Post,
    Author,
    Category,
    Library,
    LibrariesMembers,
    Borrow,
    LibraryRecord
)


class BookInline(admin.TabularInline):
    model = Book

    extra = 2
    min_num = 1
    max_num = 2

    fields = [
        'title',
        'description',
        'pages',
        'language',
        'publisher',
        'genre',
        'category',
        'libraries',
        'published_date'
    ]
    readonly_fields = ['published_date']
    ordering = ['-published_date']
    show_change_link = True
    verbose_name = "Author's Book"
    verbose_name_plural = "Author's Books"

    def formfield_for_choice_field(
            self, db_field, request, **kwargs
    ):
        if db_field.name == 'genre':
            kwargs['widget'] = admin.widgets.AdminRadioSelect()

        return super().formfield_for_choice_field(
            db_field, request, **kwargs
        )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]


class BorrowInline(admin.TabularInline):
    model = Borrow

    extra = 1

    fields = [
        'book',
        'return_date',
        'is_returned'
    ]

    ordering = [
        '-borrow_date'
    ]
    can_delete = False


@admin.register(LibraryRecord)
class LibraryRecordAdmin(admin.ModelAdmin):
    inlines = [BorrowInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'genre',
        'pages',
        'language',
        'published_date',
        'category',
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

    list_select_related = ['category', ]

    fieldsets = (
        (
            "Basic Information", {
            "fields": ("title", "description", "genre")
        }
        ),
        (
            "Publication Details", {
            "fields": ("publisher", "pages", "language"),
            "classes": ("collapse",)
        }
        ),
        (
            "Classification", {
            "fields": ("category", "libraries"),
            "classes": ("collapse",)
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
                book.title, book.genre or 'N/A', book.pages or 0, book.language, book.published_date,
                book.category.title
            ])

        return response

    @admin.action(description="Set genre to fiction")
    def set_genre_to_fiction(self, request, queryset):
        for obj in queryset:
            obj.genre = 'FICTION'
            obj.save()

        return request


class DaysOverdueFilter(admin.SimpleListFilter):
    title = 'Return status'
    parameter_name = 'return_status'

    def lookups(self, request, model_admin):
        return (
            ('returned', 'Returned'),
            ('overdue', 'Overdue'),
            ('active', 'Active'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'returned':
            return queryset.filter(is_returned=True)
        if self.value() == 'overdue':
            return queryset.filter(
                is_returned=False,
                return_date__lt=timezone.now().date()
            )
        if self.value() == 'active':
            return queryset.filter(
                is_returned=False,
                return_date__gte=timezone.now().date()
            )


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = [
        'book',
        'member_name',
        'borrow_date',
        'return_date',
        'is_returned',
        'days_overdue'
    ]

    list_filter = [
        'borrow_date',
        'return_date',
        DaysOverdueFilter
    ]

    @admin.display(description='Reader Name')
    def member_name(self, obj):
        return obj.library_record.member.last_name

    @admin.display(description='Days Overdue')
    def days_overdue(self, obj):
        if obj.is_returned:
            return mark_safe(
                '<span style="color: green;">---</span>'
            )

        today = timezone.now().date()

        if obj.return_date < today:
            overdue_days = (today - obj.return_date).days

            return format_html(
                '<span style="color: red; font-weight: bold">{} days</span>',
                overdue_days
            )

        return mark_safe(
            '<span style="color: green;">On time</span>'
        )


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(LibrariesMembers)
