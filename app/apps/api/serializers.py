from rest_framework import serializers

from apps.books.models import Book, BookLoan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre']


class BookLoanSerializer(serializers.ModelSerializer):
    days_on_hand = serializers.SerializerMethodField()

    class Meta:
        model = BookLoan
        fields = ['book', 'loan_date', 'days_on_hand']

    def get_days_on_hand(self, obj):
        return obj.days_on_hand()


class BookLoanDeleteSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()