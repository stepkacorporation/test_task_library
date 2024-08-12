from django import forms


class BookActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('borrow', 'Взять'), ('return', 'Вернуть')])
    book_id = forms.IntegerField(widget=forms.HiddenInput())
