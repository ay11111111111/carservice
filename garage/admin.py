from django.contrib import admin
from .models import Car, CarBrand, CarModel


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']

class CarAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'car_marka', 'car_model', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg']
    def get_user(self, obj):
        return obj.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'car__user'

admin.site.register(CarBrand)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
