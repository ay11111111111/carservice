from rest_framework import serializers
from ..models import Service, AutoserviceType, AutoService, Phone, OpeningHours, Review, Appointment
import datetime


def get_weekday(number):
    dict = {
        1: 'ПН',
        2: "ВТ",
        3: "СР",
        4: "ЧТ",
        5: "ПТ",
        6: "СБ",
        7: "ВС"
    }
    return dict[number]

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id','name')


class ServiceIDSerializer(serializers.Serializer):
    ids = serializers.CharField(max_length=100, required=False)


class AutoServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoService
        fields = ('id', 'name', 'type', 'address', 'rating', 'image')
        depth=1


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['phone_number']

class ScheduleSerializer(serializers.ModelSerializer):
    weekdaystr = serializers.SerializerMethodField()
    class Meta:
        model = OpeningHours
        fields = ['weekdaystr', 'working', 'worktime_from', 'worktime_till', 'lunchtime_from', 'lunchtime_till']

    def get_weekdaystr(self, obj):
        return get_weekday(obj.weekday)


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'description', 'rating', 'date']
    def get_user_name(self, obj):
        return obj.user.name_surname

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'autoservice', 'description', 'rating', 'date']

class OneAutoServiceSerializer(serializers.ModelSerializer):
    today_weekday = serializers.SerializerMethodField()
    phone_numbers = PhoneSerializer(many=True, read_only=True)
    schedule = ScheduleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = AutoService
        fields = ('id', 'name', 'type', 'address', 'rating', 'image', 'today_weekday', 'schedule', 'phone_numbers', 'reviews')
        depth = 1

    def get_today_weekday(self, obj):
        return get_weekday(datetime.date.today().weekday()+1)


class FreeSlotsSerializer(serializers.Serializer):
    date = serializers.DateField()
    times = serializers.ListField(child=serializers.TimeField())


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('autoservice', 'services', 'date', 'start_time')
