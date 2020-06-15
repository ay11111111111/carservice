from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Car, Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileCreationForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name_surname', 'phone_number']

class CarCreationForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ['car_model', 'year_of_issue','korobka', 'volume_dvigatel', 'probeg']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name_surname', 'phone_number']

# class CarCreationForm(forms.ModelForm):
#
#     class Meta:
#         model =
#
