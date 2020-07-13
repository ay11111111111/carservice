from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list', views.car_list, name='list'),
    path('<int:pk>', views.car_detail, name='detail'),
    path('<int:pk>/update', views.car_update, name='update'),
    path('carbrands', views.carbrand_list, name='carbrand-list'),
    path('carfuels', views.FuelView.as_view(), name='fuel-list'),
    path('<int:pk>/carmodels', views.carmodel_list, name='carmodel-list'),
    path('create', views.car_create, name='register'),
    path('<int:pk>/uploadimage', views.MyUploadView.as_view({'post':'create'}), name='upload-new-photo'),
    path('<int:pk>/events', views.EventView.as_view(), name='event-list'),
    path('event/<int:pk>', views.event_detail, name='detail'),
    path('<int:pk>/create-service-event', views.service_event_create, name='service'),
    path('<int:pk>/create-zapravka-event', views.zapravka_event_create, name='zapravka'),
    path('<int:pk>/create-other-event', views.other_event_create, name='other'),
    path('<int:pk>/create-calendar-event', views.CalendarEventView.as_view({'post':'create'}), name='other'),
    path('calendarevents', views.CalendarEventView.as_view({'get':'get_list'}), name='other'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
