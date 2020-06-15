from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list', views.user_list, name='list'),
    path('<int:pk>', views.user_detail, name='detail'),
    path('<int:pk>/update', views.user_update, name='update'),
    path('register', views.user_register, name='register'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
