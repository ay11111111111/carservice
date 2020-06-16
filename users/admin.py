from django.contrib import admin
from .models import CustomUser

# class CarAdmin(admin.ModelAdmin):
#     list_display = ['get_user', 'car_model', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg']
#     def get_user(self, obj):
#         return obj.user.username
#     get_user.short_description = 'User'
#     get_user.admin_order_field = 'car__user'
#
#
# admin.site.register(Car, CarAdmin)
admin.site.register(CustomUser)

# Register your models here.
