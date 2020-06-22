from django.contrib import admin
from .models import Car, CarBrand, CarModel, Event


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'brand', 'brand_id']

class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user', 'car_marka', 'car_model', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg']
    def get_user(self, obj):
        return obj.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'car__user'

class EventAdmin(admin.ModelAdmin):
    list_display = ['car', 'type', 'type_of_fuel', 'amount_of_fuel', 'name', 'money', 'probeg', 'comment', 'date']

admin.site.register(CarBrand)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Event, EventAdmin)
