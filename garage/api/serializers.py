from rest_framework import serializers
from ..models import Car, CustomUser, Event

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email')


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Car
        fields = ('id', 'car_marka', 'car_model', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg')


class ServiceEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', 'money', 'probeg', 'comment', 'date')


class ZapravkaEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'type_of_fuel', 'amount_of_fuel', 'money', 'probeg', 'comment', 'date')
