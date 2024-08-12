from django.contrib.auth import login
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import FormView
from django.views import View

from .models import CustomUser, Reader, Librarian
from .forms import UserRegistrationForm, ReaderProfileForm, LibrarianProfileForm


class UserRegisterView(FormView):
    """
    Представление для регистрации пользователей.
    """
    
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('catalog')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user and request.user.is_authenticated:
            return redirect('catalog')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        user: CustomUser = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()

        login(self.request, user)

        if user.role == CustomUser.RoleChoices.READER:
            Reader.objects.get_or_create(user=user)
            return redirect('reader_profile')
        if user.role == CustomUser.RoleChoices.LIBRARIAN:
            Librarian.objects.get_or_create(user=user)
            return redirect('librarian_profile')

        return super().form_valid(form)


class ReaderProfileView(View):
    """
    Представление для отображения и редактирования профиля читателя.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        if not hasattr(request.user, 'reader'):
            return redirect('catalog')
        form: ReaderProfileForm = ReaderProfileForm(instance=request.user.reader)
        return render(request, 'accounts/reader_profile.html', {'form': form})
    
    def post(self, request: HttpRequest) -> HttpResponse:
        if not hasattr(request.user, 'reader'):
            return redirect('catalog')
        form: ReaderProfileForm = ReaderProfileForm(request.POST, instance=request.user.reader)
        if form.is_valid():
            form.save()
            return redirect('catalog')
        return render(request, 'accounts/reader_profile.html', {'form': form})


class LibrarianProfileView(View):
    """
    Представление для отображения и редактирования профиля библиотекаря.
    """
    
    def get(self, request: HttpRequest) -> HttpResponse:
        if not hasattr(request.user, 'librarian'):
            return redirect('catalog')
        form: LibrarianProfileForm = LibrarianProfileForm(instance=request.user.librarian)
        return render(request, 'accounts/librarian_profile.html', {'form': form})
    
    def post(self, request: HttpRequest) -> HttpResponse:
        if not hasattr(request.user, 'librarian'):
            return redirect('catalog')
        form: LibrarianProfileForm = LibrarianProfileForm(request.POST, instance=request.user.librarian)
        if form.is_valid():
            form.save()
            return redirect('catalog')
        return render(request, 'accounts/librarian_profile.html', {'form': form})
