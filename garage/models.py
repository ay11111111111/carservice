from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.urls import reverse


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year
#
# def volume_choices():
#     return [(float("{0:.1f}".format(x*0.1)),float("{0:.1f}".format(x*0.1))) for x in range(11,65)]
#     # return [(x*0.1, x*0.1) for x in range(11,65)]

class Car(models.Model):
    KOROBKA_CHOICES = (
        ('auto', 'Автомат'),
        ('mech', 'Механика')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    car_model = models.CharField(max_length=60)
    year_of_issue = models.IntegerField(('Год выпуска'), choices=year_choices(), default=current_year)
    korobka = models.CharField(max_length=60, choices=KOROBKA_CHOICES, verbose_name='Коробка')
    volume_dvigatel = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Объем двигателя')
    probeg = models.IntegerField(verbose_name='Пробег')

    def get_absolute_url(self):
        return reverse('profile')
