from rest_framework import serializers
from ..models import Car, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email')


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Car
        fields = ('id', 'car_marka', 'car_model', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg')
