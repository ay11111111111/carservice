from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError
import datetime
from datetime import time
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import ugettext_lazy as _
from datetime import datetime as dt


WEEKDAYS = [
    (1, _("ПН")),
    (2, _("ВТ")),
    (3, _("СР")),
    (4, _("ЧТ")),
    (5, _("ПТ")),
    (6, _("СБ")),
    (7, _("ВС")),
]

class Service(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AutoserviceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AutoService(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(AutoserviceType, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, default='')
    address = models.CharField(max_length=255)
    rating = models.DecimalField(blank=True, default=0, max_digits=10, decimal_places=1)
    services = models.ManyToManyField(Service, related_name='services')
    cars_per_timeslot = models.IntegerField(default=1)
    image = models.ImageField(upload_to='autoservices/', verbose_name='Image')

    def __str__(self):
        return self.name


class Phone(models.Model):
    autoservice = models.ForeignKey(AutoService, on_delete=models.CASCADE, related_name='phone_numbers')
    phone_number = models.CharField(max_length=200)

    def __str__(self):
        return self.phone_number

#https://github.com/arteria/django-openinghours/blob/master/openinghours/models.py
class OpeningHours(models.Model):

    class Meta:
        verbose_name = _('Opening Hours')  # plurale tantum
        verbose_name_plural = _('Opening Hours')
        ordering = ['autoservice', 'weekday', 'worktime_from']


    autoservice = models.ForeignKey(AutoService, on_delete=models.CASCADE, related_name='schedule')
    weekday = models.IntegerField(_('День недели'), choices=WEEKDAYS)
    working = models.BooleanField(_('Рабочий день'), default=True)
    worktime_from = models.TimeField(_('Открывается'), blank=True, null=True)
    worktime_till = models.TimeField(_('Закрывается'), blank=True, null=True)
    lunchtime_from = models.TimeField(_('Обед начинается'), blank=True, null=True)
    lunchtime_till = models.TimeField(_('Обед заканчивается'), blank=True, null=True)

    def __str__(self):
        return _("%(premises)s %(weekday)s (%(worktime_from)s - %(worktime_till)s)") % {
            'premises': self.autoservice,
            'weekday': self.weekday,
            'worktime_from': self.worktime_from,
            'worktime_till': self.worktime_till
        }


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    autoservice = models.ForeignKey(AutoService, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=0)
    description = models.TextField()
    date = models.DateField(default=dt.now)

    def __str__(self):
        return self.user.email


class TimeSlot(models.Model):
    autoservice = models.ForeignKey(AutoService, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время конца')
    available = models.IntegerField(default=1, verbose_name='Свободнo мест')

    def __str__(self):
        return str(self.start_time)


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    autoservice = models.ForeignKey(AutoService, on_delete=models.CASCADE, verbose_name='СТО')
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(default='12:00')

    def clean(self):
        appointments = Appointment.objects.filter(date=self.date, autoservice=self.autoservice, start_time=self.start_time)
        if len(appointments) >= self.autoservice.cars_per_timeslot:
            raise ValidationError('Slot is not available')
