from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Author, Genre, Book, BookLoan


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'author', 'genre')
    list_filter = ('author', 'genre')
    search_fields = ('title', 'author__name', 'genre__name')
    autocomplete_fields = ('author', 'genre')


@admin.register(Book.history.model)
class HistoricalBookAdmin(admin.ModelAdmin):
    list_display = ('history_date', 'history_change_reason', 'history_type', 'title', 'author', 'genre')
    search_fields = ('title', 'author__name', 'genre__name')
    list_filter = ('history_date', 'history_change_reason', 'history_type')


@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'loan_date')
    list_filter = ('loan_date', 'reader')
    search_fields = ('book__title', 'reader__user__username')
