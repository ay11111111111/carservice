from django.urls import path, include
from . import views


urlpatterns = [
    path('url', views.URLView.as_view()),
    path('url/post', views.UrlCreateView.as_view({'post':'post'})),
]
