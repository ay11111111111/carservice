"""carservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from users import views as user_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import smart_selects
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'devices', FCMDeviceAuthorizedViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^carservice/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^carservice/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^carservice/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('carservice/', include('app.urls')),
    path('carservice/garage/', include('garage.urls')),
    path('carservice/admin/', admin.site.urls),
    path('carservice/register/', user_views.register, name="register"),
    path('carservice/login/', user_views.login_view, name="login"),
    path('carservice/logout/', user_views.logout_view, name="logout"),
    path('carservice/api/v1/auth/', include('users.api.urls')),
    path('carservice/api/v1/cars/', include('garage.api.urls')),
    path('carservice/api/v1/notification/', include('notification.api.urls')),
    url(r'^chaining/', include('smart_selects.urls')),

]
