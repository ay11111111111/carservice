from django.contrib import admin
from carservice.admin import autoserviceadmin
from .models import (Service, Phone, AutoService, Review, Appointment, TimeSlot, AutoserviceType,
                    OpeningHours)
import datetime
import calendar
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from users.models import CustomUser


class StaffRequiredAdminMixin(object):

    def check_perm(self, user_obj):
        # if not user_obj.is_active or user_obj.is_anonymous:
        #     return False
        if user_obj.is_superuser or user_obj.is_staff:
            return True
        return False

    def has_add_permission(self, request):
        return self.check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_delete_permission(self, request, obj=None):
        return self.check_perm(request.user)


class PhoneInline(admin.TabularInline):
    model = Phone

class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours

class AutoServiceForm(forms.ModelForm):

    class Meta:
        model = AutoService
        exclude = ['rating']

class AutoServiceAdmin(StaffRequiredAdminMixin,admin.ModelAdmin):
    inlines = (PhoneInline, OpeningHoursInline)
    list_display = ['name', 'type', 'address', 'email', 'rating']
    form = AutoServiceForm

    def get_queryset(self, request):

        qs = super(AutoServiceAdmin, self).get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(email=request.user.email)
        if request.user.is_superuser:
            return qs

    def save_model(self, request, obj, form, change):
        # field not editable in admin area so handle it here...
        # obj.user = request.user
        obj.save()


class AppointmentAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppointmentAdminForm, self).__init__(*args, **kwargs)
        if self.current_user.is_staff and not self.current_user.is_superuser:
            self.fields['autoservice'].queryset = AutoService.objects.filter(email=self.current_user.email)


class AppointmentAdmin(StaffRequiredAdminMixin,admin.ModelAdmin):
    list_display = ['user', 'autoservice', 'date', 'get_start_time']
    form = AppointmentAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(AppointmentAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def get_start_time(self, obj):
        return obj.start_time.strftime("%H:%M")

    def get_queryset(self, request):
        qs = super(AppointmentAdmin, self).get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(autoservice__email=request.user.email)
        if request.user.is_superuser:
            return qs

    def save_model(self, request, obj, form, change):
        # field not editable in admin area so handle it here...
        # obj.user = request.user
        obj.save()

class AutoserviceTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['autoservice', 'date', 'start_time', 'end_time', 'available']

admin.site.register(Service)
admin.site.register(AutoService, AutoServiceAdmin)
admin.site.register(Review)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(AutoserviceType, AutoserviceTypeAdmin)
admin.site.register(OpeningHours)

autoserviceadmin.register(Appointment, AppointmentAdmin)
