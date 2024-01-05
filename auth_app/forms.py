from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth import admin


class LoginForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Username', 'class': 'form-control valid'}),
        label="Username"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password', 'class': 'form-control valid'}),
        label="Password",
        validators=[
            validators.MinLengthValidator(3)
        ]
    )


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Your Username', 'class': 'form-control valid'}),
        label="Username",
        validators=[
            validators.MinLengthValidator(4, "enter more than 4 characters for username")
        ]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your email address', 'class': 'form-control valid'}),
        label="Email",
        validators=[
            validators.EmailValidator("Invalid Email Address!!")
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter Your Password', 'class': 'form-control valid'}),
        label="Password",
        validators=[
            validators.MinLengthValidator(6, "enter more than 6 characters for password")
        ]
    )
    re_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter Your Password', 'class': 'form-control valid'}),
        label="Re-Password"
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exist_user_name = User.objects.filter(username=user_name).exists()
        if is_exist_user_name:
            raise forms.ValidationError('Already Sign-In user')
        return user_name

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password != re_password:
            raise forms.ValidationError("passwords does not match!")
        return password


class EditUserForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Name', 'class': 'form-control'}),
        label='Name'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Family', 'class': 'form-control'}),
        label='Family'
    )
