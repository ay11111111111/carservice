from django.contrib import admin
from .models import (Service, Phone, AutoService, Review, Appointment, TimeSlot, AutoserviceType,
                    OpeningHours)
import datetime
import calendar
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms

class PhoneInline(admin.TabularInline):
    model = Phone

class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours

class AutoServiceForm(forms.ModelForm):
    class Meta:
        model = AutoService
        exclude = ['rating']

class AutoServiceAdmin(admin.ModelAdmin):
    inlines = (PhoneInline, OpeningHoursInline)
    list_display = ['name', 'type', 'address', 'email', 'rating']
    form = AutoServiceForm

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'autoservice', 'date', 'timeslot']

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
