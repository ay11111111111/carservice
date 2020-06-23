from django.contrib import admin
from .models import *

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at')
    search_fields = ('text', )

# class AutoAdmin(admin.ModelAdmin):
#     list_display = ('title_ru', 'text_ru', 'is_next')
#     search_fields = ('title_ru', 'text_ru', )
#     list_filter = ('category',)


class NotificationUserAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'is_viewed','get_notification')

    def get_user(self, obj):
        return obj.user.email
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__email'

    def get_notification(self, obj):
        return obj.notification.text
    get_notification.short_description = 'Notification'
    get_notification.admin_order_field = 'notification_text'

# admin.site.register(AutoNotification, AutoAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationUser, NotificationUserAdmin)
# Register your models here.
