from django.urls import path, include

from .views import UserRegisterView, ReaderProfileView, LibrarianProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),

    path('reader_profile/', ReaderProfileView.as_view(), name='reader_profile'),
    path('librarian_profile/', LibrarianProfileView.as_view(), name='librarian_profile'),
]
