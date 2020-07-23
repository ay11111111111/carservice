from ..models import Service, AutoService, Appointment, OpeningHours
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
from .filters import AutoServiceFilter
from django.utils.decorators import method_decorator
from django.db.models import Q
import datetime

class FuelView(ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()



class AutoServiceView(ListAPIView):
    serializer_class = OneAutoServiceSerializer
    # permission_classes = (IsAuthenticated,)
    # filter_backends = [DjangoFilterBackend]
    queryset = AutoService.objects.all()
    # filterset_class = AutoServiceFilter


class AutoServiceOneView(viewsets.GenericViewSet):
    serializer_class = OneAutoServiceSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            autoservice = AutoService.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(autoservice)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AutoServiceFilteredView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ServiceIDSerializer

    def post(self, request, format=None):
        serializer = ServiceIDSerializer(data=request.data)
        if serializer.is_valid():
            ids = serializer.data['ids']
            arr_ids = [int(x) for x in ids.split(',')]
            # AutoServices = AutoService.objects.filter(services__in=arr_ids).distinct()  --- OR
            AutoServices = AutoService.objects.filter(services__id=arr_ids[0])
            if len(arr_ids)>1:
                for id in range(1, len(arr_ids)):
                    AutoServices.filter(services__id=id)
            serializer2 = AutoServiceSerializer(AutoServices, many=True)
            return Response(data=serializer2.data)
        return Response(serializer.errors)


class ReviewCreateView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewCreateSerializer

    def create(self, request, format=None):
        user = request.user
        print(user)
        review = Review(user=user)
        serializer = self.serializer_class(review, data=request.data)
        data={}
        if serializer.is_valid():
            review = serializer.save()
            data['id'] = review.id
            data['response'] = 'successfully created new review'
            data['user'] = review.user.name_surname
            data['autoservice'] = review.autoservice.name
            data['description'] = review.description
            data['rating'] = review.rating
        else:
            data = serializer.errors

        return Response(data)

def get_free_times(date, autoservice):
    appointments = Appointment.objects.filter(autoservice=autoservice, date=date)
    weekday = date.weekday() + 1
    openinghours = OpeningHours.objects.get(autoservice=autoservice, weekday=weekday)
    if openinghours.working:
        return []

class FreeSlotsView(viewsets.GenericViewSet):
    # permission_classes = (AllowAny,)
    serializer_class = FreeSlotsSerializer

    def get(self, request, pk, format=None):
        autoservice = AutoService.objects.get(pk=pk)
        datenow = datetime.date.today()
        #date = datetime.date.today()+datetime.timedelta(days=i)
        data = []
        for i in range(4):
            date = datetime.date.today()+datetime.timedelta(days=i)
            times = get_free_times(date, autoservice)
            data.append({"date":date})
        hz = [
              {
                "date":"01.05.2020",
                "times":[
                  "10:00",
                  "11:00",
                  "16:00",
                  "22:00"
                ]
              },
              {
                "date":"02.05.2020",
                "times":[
                  "10:00",
                  "11:00",
                  "16:00",
                  "22:00"
                ]
              },
              {
                "date":"03.05.2020",
                "times":[
                  "10:00",
                  "11:00",
                  "16:00",
                  "22:00"
                ]
              },
              {
                "date":"04.05.2020",
                "times":[
                  "10:00",
                  "11:00",
                  "16:00",
                  "22:00"
                ]
              }
            ]
        return Response(data)
