from rest_framework import serializers
from ..models import Car, CustomUser, Event, CarModel, CarBrand, CarImages, CalendarEvent, Fuel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email')


class CarImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarImages
        fields = ('id', 'image')


class CarCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer
    title = serializers.SerializerMethodField('get_title')

    def get_title(self,obj):
        return obj.car_marka.name + ' ' + obj.car_model.name

    class Meta:
        model = Car
        fields = ('id', 'car_marka', 'car_model', 'title', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg', 'rashod_topliva')


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer
    title = serializers.SerializerMethodField('get_title')
    carimagess = CarImgSerializer(many=True, read_only=True)

    def get_title(self,obj):
        return obj.car_marka.name + ' ' + obj.car_model.name

    class Meta:
        model = Car
        fields = ('id', 'car_marka', 'car_model', 'title', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg', 'rashod_topliva', 'carimagess')
        depth = 2

class ServiceEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', 'money', 'probeg', 'comment', 'date')


class ZapravkaEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'type_of_fuel', 'amount_of_fuel', 'money', 'probeg', 'comment', 'date')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class CalendarEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalendarEvent
        fields = ('id', 'name', 'place', 'date')

class CarBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrand
        fields = ('id', 'name')


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = ('id', 'name')


class FuelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fuel
        fields = ('id', 'name')
