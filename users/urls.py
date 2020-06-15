from django.contrib import admin
from django.urls import path, include
from .views import (CarCreateView, ProfileCreateView,
                    CarDetailView,
                    CarUpdateView,
                    CarDeleteView)

urlpatterns = [
    path('car/create/', CarCreateView.as_view(), name='car-create'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car-update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car-delete'),
    path('create/', ProfileCreateView.as_view(), name='profile-create'),

]
