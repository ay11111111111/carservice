from rest_framework import serializers
from ..models import Notification, NotificationUser, FCMDevice


class NotificationSerializer(serializers.ModelSerializer):
    is_viewed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'

    def get_is_viewed(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            return NotificationUser.objects.get(user=user, notification=instance).is_viewed
        return False


class NotificationPushSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationActionSerializer(serializers.Serializer):
    notifications = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = '__all__'


class FCMDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMDevice
        fields = ('registration_id', 'device_id', 'type')
