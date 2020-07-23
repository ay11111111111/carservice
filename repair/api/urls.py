from django.urls import path, include
from . import views
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

# decorated_cto_view = \
#    swagger_auto_schema(
#       method='get',
#       responses={status.HTTP_200_OK:CTOSerializer},
#       operation_description='Input: id numbers dvided by comma. Ex.: 1,2,3'
#    )(views.CTOfilteredView.as_view())

urlpatterns = [
    path('services', views.FuelView.as_view()),
    path('autoservices', views.AutoServiceFilteredView.as_view({'post':'post'})),
    path('autoservices/<int:pk>', views.AutoServiceOneView.as_view({'get':'get'})),
    path('reviews/create', views.ReviewCreateView.as_view({'post':'create'})),
]
