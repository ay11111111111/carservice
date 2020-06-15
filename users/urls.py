from django.contrib import admin
from django.urls import path, include
from .views import (ProfileCreateView,
                    )

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='profile-create'),

]
