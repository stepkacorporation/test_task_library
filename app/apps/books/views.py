from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.db.models import Q
from django.utils import timezone

from apps.accounts.models import Reader, CustomUser
from .models import Book, BookLoan


class CatalogView(LoginRequiredMixin, View):
    template_name = 'books/catalog.html'

    def get(self, request, *args, **kwargs):
        user: CustomUser = request.user
        
        if user.role == CustomUser.RoleChoices.LIBRARIAN:
            return redirect('overdue_books')

        loaned_books = BookLoan.objects.filter(reader__user=user).values_list('book_id', flat=True)
        books = Book.objects.filter(
            Q(bookloan__reader__user=user) | Q(bookloan__isnull=True)
        ).distinct().order_by('title')
        
        context = {
            'books': books,
            'loaned_books': loaned_books,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        reader, created = Reader.objects.get_or_create(user=user)

        if not reader.is_profile_complete():
            loaned_books = BookLoan.objects.filter(reader__user=user).values_list('book_id', flat=True)
            books = Book.objects.filter(
                Q(bookloan__reader__user=user) | Q(bookloan__isnull=True)
            ).distinct().order_by('title')

            context = {
                'books': books,
                'loaned_books': loaned_books,
                'error_message': 'Пожалуйста, заполните все поля профиля, прежде чем брать книги.',
            }
            return render(request, self.template_name, context)

        loan, created = BookLoan.objects.get_or_create(book=book, reader=reader)

        if not created:
            loan.delete()

        return redirect('catalog')


class MyBooksView(LoginRequiredMixin, View):
    template_name = 'books/my_books.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        loans = BookLoan.objects.filter(reader__user=user).order_by('book__title')

        loan_data = []
        for loan in loans:
            loan_data.append({
                'book_title': loan.book.title,
                'book_id': loan.book.id,
                'loan_date': loan.loan_date,
                'days_on_hand': loan.days_on_hand,
            })

        context = {
            'loan_data': loan_data,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            loan = BookLoan.objects.filter(book=book, reader__user=request.user).first()
            if loan:
                loan.delete()
                return redirect('my_books')

        return self.get(request, *args, **kwargs)
    

class OverdueBooksView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BookLoan
    template_name = 'books/overdue_books.html'
    context_object_name = 'overdue_data'
    
    def test_func(self):
        return self.request.user.role == CustomUser.RoleChoices.LIBRARIAN

    def get_queryset(self):
        overdue_loans = BookLoan.objects.all()
        
        overdue_data = []
        for loan in overdue_loans:
            overdue_data.append({
                'username': loan.reader.user.username,
                'first_name': loan.reader.first_name,
                'last_name': loan.reader.last_name,
                'address': loan.reader.address,
                'book_title': loan.book.title,
                'loan_date': loan.loan_date,
                'days_on_hand': loan.days_on_hand(),
            })
        
        return overdue_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overdue_data'] = self.get_queryset()
        return context