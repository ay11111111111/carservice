from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError


class Service(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AutoserviceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CTO(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(AutoserviceType, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, default='')
    address = models.CharField(max_length=255)
    rating = models.DecimalField(blank=True, default=0, max_digits=10, decimal_places=1)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    services = models.ManyToManyField(Service)
    cars_per_timeslot = models.IntegerField(default=1)
    morning_bound_workday = models.TimeField(default='9:00')
    evening_bound_workday = models.TimeField(default='20:00')
    lunch_from = models.TimeField(default='13:00')
    lunch_to = models.TimeField(default='14:00')
    morning_bound_saturday = models.TimeField(default='9:00')
    evening_bound_saturday = models.TimeField(default='20:00')
    morning_bound_sunday = models.TimeField(default='9:00')
    evening_bound_sunday = models.TimeField(default='20:00')


    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    cto = models.ForeignKey(CTO, on_delete=models.CASCADE, verbose_name='СТО')
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Время начала')

    # def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
    #     overlap = False
    #     if new_start == fixed_end or new_end == fixed_start:
    #         overlap = False
    #     elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
    #         overlap = True
    #     elif new_start <= fixed_start and new_end >= fixed_end:
    #         overlap = True
    #
    #     return overlap
    #
    #
    def clean(self):
        # if self.end_time <= self.start_time:
        #     raise ValidationError('Ending times must after starting times')

        appointments = Appointment.objects.filter(date=self.date, cto=self.cto, start_time=self.start_time)
        if len(appointments) >= self.cto.cars_per_timeslot:
            raise ValidationError('Slot is not available')
        #
        # if appointments.exists():
        #     for app in appointments:
        #         if self.check_overlap(app.start_time, app.end_time, self.start_time, self.end_time):
        #             raise ValidationError(
        #                 'There is an overlap with another event: ' + str(app.date) + ', ' + str(
        #                     app.start_time) + '-' + str(app.end_time))

class TimeSlot(models.Model):
    cto = models.ForeignKey(CTO, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время конца')
    availability = models.BooleanField(default=True, verbose_name='Свободный')


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CTO = models.ForeignKey(CTO, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    message = models.TextField()

    def __str__(self):
        return self.user.email
