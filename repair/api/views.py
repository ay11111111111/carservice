from ..models import Service, CTO
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CtoFilter
from django.utils.decorators import method_decorator
from django.db.models import Q


class FuelView(ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()



class CTOView(ListAPIView):
    serializer_class = CTOSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    queryset = CTO.objects.all()
    filterset_class = CtoFilter


class CTOfilteredView(viewsets.GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ServiceIDSerializer

    def post(self, request, format=None):
        serializer = ServiceIDSerializer(data=request.data)
        if serializer.is_valid():
            ids = serializer.data['ids']
            arr_ids = [int(x) for x in ids.split(',')]
            # ctos = CTO.objects.filter(services__in=arr_ids).distinct()  --- OR
            ctos = CTO.objects.filter(services__id=arr_ids[0])
            if len(arr_ids)>1:
                for id in range(1, len(arr_ids)):
                    ctos.filter(services__id=id)
            serializer2 = CTOSerializer(ctos, many=True)
            return Response(data=serializer2.data)
        return Response(serializer.errors)
