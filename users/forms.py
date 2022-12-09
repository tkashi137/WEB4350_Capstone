from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'inputEmail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'inputPassword1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'inputPassword2'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'id': 'inputUsername'
            }),
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'id': 'inputFirstName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'id': 'inputLastName'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'type': "email",
                'id': 'inputEmail'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': "form-control",
                'type': 'password',
                'id': 'inputPassword1'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': "form-control",
                'type': 'password',
                'id': 'inputPassword2'
            }),
        }
# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']




