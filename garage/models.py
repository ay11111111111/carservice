from django.db import models
from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.urls import reverse


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year


class Car(models.Model):
    KOROBKA_CHOICES = (
        ('auto', 'Автомат'),
        ('mech', 'Механика')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    car_model = models.CharField(max_length=60)
    year_of_issue = models.IntegerField(('Год выпуска'), choices=year_choices(), default=current_year)
    korobka = models.CharField(max_length=60, choices=KOROBKA_CHOICES, verbose_name='Коробка')
    volume_dvigatel = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Объем двигателя')
    probeg = models.IntegerField(verbose_name='Пробег')

    def get_absolute_url(self):
        return reverse('profile')
