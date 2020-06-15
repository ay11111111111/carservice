from rest_framework import serializers
from ..models import Car
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CarSerializer(serializers.ModelSerializer):
    user_id = UserSerializer
    class Meta:
        model = Car
        fields = ('id', 'user_id', 'car_model', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg')
