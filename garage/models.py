from django.db import models
from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
import datetime, os, json
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey
from datetime import datetime as dt

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]


def current_year():
    return datetime.date.today().year


def get_model_choices(car_marka):
    with open(os.path.dirname(__file__)+'/json_data/car-list.json') as f:
        car_list = json.load(f)
    for car in car_list:
        if car["brand"]==car_marka:
            return [(model, model) for model in car["models"]]


class CarBrand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Car(models.Model):
    KOROBKA_CHOICES = (
        ('auto', 'Автомат'),
        ('mech', 'Механика')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    car_marka = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    car_model = ChainedForeignKey(
        CarModel,
        chained_field='car_marka',
        chained_model_field='brand',
        show_all=True,
        auto_choose=True,
        sort=True
    )
    year_of_issue = models.IntegerField(('Год выпуска'), choices=year_choices(), default=current_year)
    korobka = models.CharField(max_length=60, choices=KOROBKA_CHOICES, verbose_name='Коробка')
    volume_dvigatel = models.DecimalField(default=0, max_digits=10, decimal_places=1, verbose_name='Объем двигателя')
    probeg = models.IntegerField(verbose_name='Пробег')

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self):
        return self.user.email + '\'s ' + self.car_marka.name + ' ' + self.car_model.name

class Event(models.Model):
    EVENT_CHOICES = (
        ('zapravka', 'Заправка'),
        ('service', 'Сервис'),
        ('other', 'Другое')
    )
    FUEL_CHOICES = (
        ('80', 'АИ-80'),
        ('92', 'АИ-92'),
        ('93', 'АИ-93'),
        ('95', 'АИ-95'),
        ('98', 'АИ-98'),
        ('diesel', 'ДТ')
    )

    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')
    type = models.CharField(max_length=60, choices=EVENT_CHOICES, verbose_name='Тип')
    type_of_fuel = models.CharField(blank=True, max_length=60, choices=FUEL_CHOICES, verbose_name='Вид топлива')
    amount_of_fuel = models.IntegerField(blank=True, default=0, verbose_name='Количество л.')
    name = models.CharField(max_length=100, verbose_name='Название', blank=True)
    money = models.IntegerField(verbose_name='Сумма')
    probeg = models.IntegerField(verbose_name="Пробег")
    comment = models.CharField(max_length=200, verbose_name='Комментарий', blank=True)
    date = models.DateTimeField(default=dt.now, blank=True, verbose_name='Дата и время')
