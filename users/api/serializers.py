from rest_framework import serializers
from ..models import CustomUser, TechSupport
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'name_surname', 'phone_number')

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2')
        extra_kwargs = {
                'password':{'write_only': True}
        }

    def save(self):
        user = CustomUser(
                email=self.validated_data['email'],
            )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password!=password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm = serializers.CharField()
    old_password = serializers.CharField()

    def is_equal(self, data):
        return data['password'] == data['confirm']


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name_surname', 'phone_number')

class TechSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechSupport
        fields = ('email', 'phone_number', 'message')
