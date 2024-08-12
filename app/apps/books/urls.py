from django.urls import path
from .views import CatalogView, MyBooksView, OverdueBooksView

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('my-books/', MyBooksView.as_view(), name='my_books'),
    path('overdue/', OverdueBooksView.as_view(), name='overdue_books'),
]
