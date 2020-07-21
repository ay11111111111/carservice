from django.urls import path, include
from . import views
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import CTOSerializer

# decorated_cto_view = \
#    swagger_auto_schema(
#       method='get',
#       responses={status.HTTP_200_OK:CTOSerializer},
#       operation_description='Input: id numbers dvided by comma. Ex.: 1,2,3'
#    )(views.CTOfilteredView.as_view())

urlpatterns = [
    path('services', views.FuelView.as_view()),
    path('autoservices', views.CTOfilteredView.as_view({'post':'post'})),
]
