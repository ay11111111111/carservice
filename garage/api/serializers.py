from rest_framework import serializers
from ..models import Car, CustomUser, Event, CarModel, CarBrand


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email')


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer
    title = serializers.SerializerMethodField('get_title')

    def get_title(self,obj):
        return obj.car_marka.name + ' ' + obj.car_model.name


    class Meta:
        model = Car
        fields = ('id', 'car_marka', 'car_model', 'title', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg')


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


class CarBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrand
        fields = ('id', 'name')


class CarModelSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField('get_brand')
    def get_brand(self, obj):
        return obj.brand.name

    brand_id = serializers.SerializerMethodField('get_brandid')
    def get_brandid(self, obj):
        return obj.brand.id

    class Meta:
        model = CarModel
        fields = ('id', 'brand_id', 'brand', 'name')
