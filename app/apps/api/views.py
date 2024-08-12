from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from apps.books.models import Book, BookLoan, Reader
from .serializers import BookSerializer, BookLoanSerializer, BookLoanDeleteSerializer


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.all()


class BookLoanCreateView(generics.CreateAPIView):
    serializer_class = BookLoanSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        reader = get_object_or_404(Reader, user=request.user)
        book_id = request.data.get('book_id')
        
        book = get_object_or_404(Book, id=book_id)

        if BookLoan.objects.filter(book=book, reader=reader).exists():
            return Response({'detail': 'Книга уже взята'}, status=status.HTTP_400_BAD_REQUEST)

        loan = BookLoan(book=book, reader=reader)
        loan.save()
        return Response(BookLoanSerializer(loan).data, status=status.HTTP_201_CREATED)


class BookLoanDeleteView(generics.DestroyAPIView):
    serializer_class = BookLoanDeleteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        reader = get_object_or_404(Reader, user=request.user)
        book = get_object_or_404(Book, id=book_id)

        try:
            loan = BookLoan.objects.get(book=book, reader=reader)
            loan.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BookLoan.DoesNotExist:
            return Response({'detail': 'Вы не взяли эту книгу'}, status=status.HTTP_400_BAD_REQUEST)


class BookLoanListView(generics.ListAPIView):
    serializer_class = BookLoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        reader = get_object_or_404(Reader, user=self.request.user)
        return BookLoan.objects.filter(reader=reader)
