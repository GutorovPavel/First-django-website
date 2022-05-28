from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from django import forms


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'

