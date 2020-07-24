from django.urls import path, include
from . import views
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


urlpatterns = [
    path('services', views.FuelView.as_view()),
    path('autoservices', views.AutoServiceFilteredView.as_view({'post':'post'})),
    path('autoservices/<int:pk>', views.AutoServiceOneView.as_view({'get':'get'})),
    path('reviews/create', views.ReviewCreateView.as_view({'post':'create'})),
    path('autoservices/<int:pk>/freeslots', views.FreeSlotsView.as_view({'get':'get'})),
    path('appointment/create', views.AppointmentCreateView.as_view({'post':'create'})),

]
