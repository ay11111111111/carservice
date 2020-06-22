from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('<int:pk>', views.car_detail, name='detail'),
    path('<int:pk>/update', views.car_update, name='detail'),
    path('create', views.car_create, name='register'),
    path('<int:pk>/create-service-event', views.service_event_create, name='service'),
    path('<int:pk>/create-zapravka-event', views.zapravka_event_create, name='zapravka'),
    path('<int:pk>/create-other-event', views.other_event_create, name='other'),

]


urlpatterns = format_suffix_patterns(urlpatterns)
