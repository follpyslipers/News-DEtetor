# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-lg'})
        self.fields['email'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-lg'})
        self.fields['password1'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-lg'})
        self.fields['password2'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-lg'})

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-lg'})
        self.fields['password'].widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-lg'})