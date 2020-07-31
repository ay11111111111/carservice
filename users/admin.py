from django.contrib import admin
from .models import CustomUser, TechSupport
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_admin', 'is_staff')

    def clean_password(self):
        return self.initial["password"]

# class MyUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
#         exclude = ['date_joined', 'last_login']


class TechSupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number', 'message']

# admin.site.unregister(CustomUser)

# @admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (('None', {'fields':('email', 'groups', 'permissions', 'name_surname', 'phone_number', 'is_admin', 'is_active', 'is_staff', 'is_superuser', )},),)
    fieldsets = (('None', {'fields':('email', 'groups', 'permissions', 'name_surname', 'phone_number', 'is_admin', 'is_active', 'is_staff', 'is_superuser',)},),)
    form = UserChangeForm
    add_form = UserCreationForm
    model = CustomUser

    list_display = ['id', 'email']
    ordering = ('email',)

admin.site.register(CustomUser)
admin.site.register(TechSupport, TechSupportAdmin)

# Register your models here.
