from ..models import Shop
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from drf_yasg import openapi


class UrlCreateView(viewsets.GenericViewSet):
    serializer_class = ShopSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            shop = Shop.objects.get(pk=1)
            shop.url = serializer.data['url']
            shop.save()
            data['url'] = shop.url
            data['response'] = 'successfully created url'
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class URLView(ListAPIView):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
