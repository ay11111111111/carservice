from django.db import models
from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
import datetime, os, json
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey
from datetime import datetime as dt
from django_unixdatetimefield import UnixDateTimeField
from carservice.settings import MEDIA_ROOT


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
    logo = models.ImageField(upload_to='logos/', default='default.png', blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        try:
            return self.toJSON()
        except:
            return self.__dict__


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
    year_of_issue = models.CharField(max_length=5, verbose_name='Год выпуска')
    korobka = models.CharField(max_length=60, verbose_name='Коробка')
    volume_dvigatel = models.DecimalField(default=0, max_digits=10, decimal_places=1, verbose_name='Объем двигателя')
    probeg = models.IntegerField(verbose_name='Пробег', default=0)
    rashod_topliva = models.IntegerField(verbose_name='Расход топлива', default=0)
    current_vol = models.IntegerField(verbose_name='Текущее кол-во топлива', default=0)

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self):
        return self.user.email + '\'s ' + self.car_marka.name + ' ' + self.car_model.name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def __repr__(self):
        return self.toJSON()

    def get_upload_to(self, filename):
        folder_name = 'images'
        filename = self.file.field.storage.get_valid_name(filename)
        return os.path.join(folder_name, filename)


class CarImages(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='carimagess')
    image = models.ImageField(upload_to='images/', verbose_name='Image')

    def __str__(self):
        #return self.car.user.email + '\'s ' + self.car.car_marka.name + ' ' + self.car.car_model.name
        return str(MEDIA_ROOT) + '/' + str(self.image)

class Fuel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_CHOICES = (
        ('zapravka', 'Заправка'),
        ('service', 'Сервис'),
        ('other', 'Другое')
    )

    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')
    type = models.CharField(max_length=60, choices=EVENT_CHOICES, verbose_name='Тип')
    type_of_fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Вид топлива')
    amount_of_fuel = models.IntegerField(blank=True, default=0, verbose_name='Количество л.')
    current_amount_of_fuel = models.IntegerField(blank=True, default=0, verbose_name='Текущее кол-во топлива')
    name = models.CharField(max_length=100, verbose_name='Название', blank=True)
    money = models.IntegerField(verbose_name='Сумма')
    probeg = models.IntegerField(verbose_name="Пробег")
    comment = models.CharField(max_length=200, verbose_name='Комментарий', blank=True)
    date = models.DateTimeField(default=dt.now, blank=True, verbose_name='Дата и время')
    #date = UnixDateTimeField()

class CalendarEvent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название')
    place = models.CharField(max_length=200, verbose_name='Место')
    date = models.DateTimeField(verbose_name='Дата')
    # date = UnixDateTimeField()

    def __str__(self):
        return self.name
