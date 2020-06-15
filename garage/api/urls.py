from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list', views.car_list, name='list'),
    path('<int:pk>', views.car_detail, name='detail'),
    path('<int:pk>/update', views.car_update, name='detail'),
    path('create', views.car_create, name='register'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
