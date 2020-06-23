from django.urls import path
from .views import *

urlpatterns = [
    path('list/', NotificationList.as_view()),
    # path('auto/', AutoView.as_view()),
    path('count/', NotificationViewSet.as_view({'get':'count'})),
    path('read/', NotificationViewSet.as_view({'post':'read'})),
    path('delete/', NotificationViewSet.as_view({'post':'delete'})),
    path('device/register/', FCMRegistration.as_view({'post':'create'})),
]
