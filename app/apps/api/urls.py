from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import BookListView, BookLoanCreateView, BookLoanDeleteView, BookLoanListView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('books/', BookListView.as_view(), name='book-list'),
    path('books/loan/', BookLoanCreateView.as_view(), name='book-loan'),
    path('books/return/<int:book_id>/', BookLoanDeleteView.as_view(), name='book-return'),
    path('books/loans/', BookLoanListView.as_view(), name='book-loan-list'),
]
