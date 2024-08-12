from django.core.management.base import BaseCommand

from apps.books.models import Author, Genre, Book


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        authors = [
            'Фёдор Михайлович Достоевский',
            'Лев Николаевич Толстой',
            'Антон Павлович Чехов',
            'Александр Сергеевич Пушкин',
            'Иван Тургенев'
        ]

        genres = [
            'Роман',
            'Повесть',
            'Рассказы',
            'Поэзия',
            'Драма'
        ]

        for genre in genres:
            Genre.objects.get_or_create(name=genre)

        for author in authors:
            Author.objects.get_or_create(name=author)

        books = [
            {'title': 'Преступление и наказание', 'author': 'Фёдор Михайлович Достоевский', 'genre': 'Роман'},
            {'title': 'Война и мир', 'author': 'Лев Николаевич Толстой', 'genre': 'Роман'},
            {'title': 'Чайка', 'author': 'Антон Павлович Чехов', 'genre': 'Драма'},
            {'title': 'Евгений Онегин', 'author': 'Александр Сергеевич Пушкин', 'genre': 'Поэзия'},
            {'title': 'Отцы и дети', 'author': 'Иван Тургенев', 'genre': 'Роман'}
        ]

        for book in books:
            author = Author.objects.get(name=book['author'])
            genre = Genre.objects.get(name=book['genre'])
            Book.objects.get_or_create(
                title=book['title'],
                author=author,
                genre=genre
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data.'))
