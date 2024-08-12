from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Librarian, Reader


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'usable_password' in self.fields:
            del self.fields['usable_password']

    
class ReaderProfileForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ('first_name', 'last_name', 'address',)


class LibrarianProfileForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = ('employee_id',)


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
