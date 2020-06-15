from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.urls import reverse


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_surname = models.CharField(max_length=60)
    phone_number = PhoneNumberField(default='')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class Car(models.Model):
    KOROBKA_CHOICES = (
        ('auto', 'Автомат'),
        ('mech', 'Механика')
    )
    VOLUME_CHOICES = ([(float("{0:.2f}".format(x*0.1)),float("{0:.2f}".format(x*0.1))) for x in range(11,65)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    car_model = models.CharField(max_length=60)
    year_of_issue = models.IntegerField(('Год выпуска'), choices=year_choices(), default=current_year)
    korobka = models.CharField(max_length=60, choices=KOROBKA_CHOICES, verbose_name='Коробка')
    volume_dvigatel = models.DecimalField(max_digits=3, decimal_places=1, choices=VOLUME_CHOICES, verbose_name='Объем двигателя')
    probeg = models.IntegerField(verbose_name='Пробег')

    def get_absolute_url(self):
        return reverse('profile')
