from rest_framework import serializers
from ..models import Notification, NotificationUser
from django.db.models.signals import post_save
from fcm_django.models import FCMDevice
from users.models import CustomUser
from django.dispatch import receiver

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

def send_to_topic(data, device):
    device.send_message(title=data['title'], body=data['text'], data=data, sound="default")

@receiver(post_save, sender=Notification)
def notification_handler(sender, instance, created, **kwargs):
    if created:
        users = CustomUser.objects.all()
        for user in users:
            NotificationUser.objects.create(user=user, notification=instance)
        serializer = NotificationPushSerializer(instance)
        device = FCMDevice.objects.filter(active=True)
        print(device.count())
        send_to_topic(serializer.data, device)
