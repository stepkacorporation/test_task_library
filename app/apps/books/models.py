from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from apps.accounts.models import Reader


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='ФИО')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')

    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('title',)


class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='Читатель')
    loan_date = models.DateField(auto_now_add=True, verbose_name='Дата получения книги')

    def __str__(self) -> str:
        return f"{self.reader.user.username} - {self.book.title}"

    class Meta:
        verbose_name = 'Выдача книги'
        verbose_name_plural = 'Выдача книг'
        unique_together = ('book', 'reader')

    def days_on_hand(self):
        return (timezone.now().date() - self.loan_date).days

