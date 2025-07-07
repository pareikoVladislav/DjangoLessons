from django.contrib import admin

from src.library.models import Borrow


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    #В списке отображать: книгу, участника, дату выдачи, дату возврата, статус
    list_display = [
        'book',  # Название книги
        'library_record',  # Имя участника и библиотеки
        'borrow_date',
        'return_date',
        'is_returned'  # Статус возврата
    ]

    #Реализовать фильтрацию по статусу возврата, дате выдачи, дате возврата
    list_filter = [
        'is_returned',
        'borrow_date',
        'return_date'
    ]

    #Добавить поиск по названию книги и имени участника
    search_fields = [
        'book__title',
        'library_record__member__last_name'
    ]
    #Сделать поле статуса редактируемым прямо в списке
    list_editable = ['is_returned']

    #Настроить пагинацию с отображением 30 записей на странице
    list_per_page = 30

    #Создать группировку полей: "Информация о займе", "Даты", "Статус"
    fieldsets = (
        ("Информация о займе", {
            "fields": ("book", "library_record")
        }),
        ("Даты", {
            "fields": ("borrow_date", "return_date"),
            "classes": ("collapse",)
        }),
        ("Статус", {
            "fields": ("is_returned",),
            "classes": ("collapse",)
        }),
    )
    # @admin.display(description='')
    # def admin_display
