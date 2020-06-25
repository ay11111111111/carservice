from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError



# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password1', 'password2']

class CustomUserCreationForm(forms.Form):

    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class CustomAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password')#, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid login")
        #     else:
        #         self.confirm_login_allowed(self.user_cache)
        # return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']

# 
# class ProfileCreationForm(forms.ModelForm):
#
#     class Meta:
#         model = Profile
#         fields = ['name_surname', 'phone_number']


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['name_surname', 'phone_number']
