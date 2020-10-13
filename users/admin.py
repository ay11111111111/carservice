from django.contrib import admin
from .models import CustomUser, TechSupport
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class TechSupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number', 'message']

# admin.site.unregister(CustomUser)

# @admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_superuser', 'is_admin', 'is_staff']
    # exclude = ['date_joined', 'last_login', 'username']
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TechSupport, TechSupportAdmin)

# Register your models here.
