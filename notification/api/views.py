from ..models import Notification, NotificationUser
from fcm_django.models import FCMDevice
from users.models import CustomUser
from .serializers import (NotificationSerializer,
                        NotificationPushSerializer,
                        NotificationActionSerializer,
                        FCMDeviceSerializer)
from django.db.models.signals import post_save
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

# HEADER_PARAM = openapi.Parameter('Authorization', openapi.IN_HEADER,  description="Example: Token <string>", type=openapi.TYPE_STRING)


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

    @swagger_auto_schema(operation_description="")
    def count(self, request):
        count = NotificationUser.objects.filter(user=request.user, is_viewed=False).count()
        return Response({'count':count})

    @swagger_auto_schema(operation_description="")
    def read(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            NotificationUser.objects.filter(user=request.user, notification_id__in=data['notifications']).update(is_viewed=True)
            return Response({'message':'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="")
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

    @swagger_auto_schema(operation_description="")
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
        except:
            serializer = self.serializer_class(data=data, many=False)
            if serializer.is_valid():
                serializer.save(user=request.user, active=True)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
