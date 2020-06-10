from django import forms
from django.contrib.auth.models import User
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class SignupForm(forms.ModelForm):
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())

    field_order = ['username', 'password', 'password_check', 'last_name',
                   'first_name', 'email']

    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password', 'last_name', 'first_name', 'email']


class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password']
