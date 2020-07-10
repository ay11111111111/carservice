from django.contrib import admin
from .models import CustomUser, TechSupport

class TechSupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number', 'message']


admin.site.register(CustomUser)
admin.site.register(TechSupport, TechSupportAdmin)

# Register your models here.
