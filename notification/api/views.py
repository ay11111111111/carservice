from ..models import Notification, NotificationUser, FCMDevice
from users.models import CustomUser
from .serializers import (NotificationSerializer,
                        NotificationPushSerializer,
                        NotificationActionSerializer,
                        FCMDeviceSerializer)
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

HEADER_PARAM = openapi.Parameter('Authorization', openapi.IN_HEADER,  description="Example: Token <string>", type=openapi.TYPE_STRING)

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
            send_to_topic(serializer.data, device)


class NotificationList(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Notification.objects.filter(user_notification__user=self.request.user)
        return Notification.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class NotificationViewSet(GenericViewSet):
    serializer_class = NotificationActionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(operation_description="", manual_parameters=[HEADER_PARAM])
    def count(self, request):
        count = NotificationUser.objects.filter(user=request.user, is_viewed=False).count()
        return Response({'count':count})

    @swagger_auto_schema(operation_description="", manual_parameters=[HEADER_PARAM])
    def read(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            NotificationUser.objects.filter(user=request.user, notification_id__in=data['notifications']).update(is_viewed=True)
            return Response({'message':'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="", manual_parameters=[HEADER_PARAM])
    def delete(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            NotificationUser.objects.filter(user=request.user, notification_id__in=data['notifications']).delete()
            return Response({'message':'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FCMRegistration(GenericViewSet):
    serializer_class = FCMDeviceSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(operation_description="", manual_parameters=[HEADER_PARAM])
    def create(self, request):
        data = request.data
        try:
            fcm_device = FCMDevice.objects.get(user=request.user)
            serializer = self.serializer_class(fcm_device, data=data, partial=True, many=False)
            if serializer.is_valid():
                serializer.save(active=True)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FCMDevice.DoesNotExist:
            serializer = self.serializer_class(data=data, many=False)
            if serializer.is_valid():
                serializer.save(user=request.user, active=True)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
