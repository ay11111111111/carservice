from rest_framework import serializers
from ..models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
                'password':{'write_only': True}
        }

    def save(self):
        user = User(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
            )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password!=password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('name_surname', 'phone_number')

#
# class CarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Car
#         fields = ('user', 'car_model', 'year_of_issue', 'korobka', 'volume_dvigatel', 'probeg')
