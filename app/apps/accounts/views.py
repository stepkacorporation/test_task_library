from django.contrib.auth import login, authenticate, logout
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth.views import LoginView


from .models import CustomUser, Reader, Librarian
from .forms import UserRegistrationForm, ReaderProfileForm, LibrarianProfileForm, UserLoginForm


class UserRegisterView(FormView):
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


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('catalog')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user and request.user.is_authenticated:
            return redirect('catalog')
        return super().dispatch(request, *args, *kwargs)

    def form_valid(self, form: UserLoginForm) -> HttpResponse:
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return self.form_invalid(form)