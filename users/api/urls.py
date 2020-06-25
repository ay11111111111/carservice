from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
#    path('list', views.user_list, name='list'),
    path('profile', views.user_detail, name='detail'),
    path('profile/create', views.profile_create, name='profile-create'),
    path('profile/update', views.user_update, name='update'),
    path('register', views.user_register, name='register'),
    path('login', views.CustomAuthTokenAPI.as_view(), name='login'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
