from django.db import models
from fcm_django.models import FCMDevice
from users.models import CustomUser
# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=250, default='Новое уведомление')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_at',)


class NotificationUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notification_to_user')
    is_viewed = models.BooleanField(default=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='user_notification')
