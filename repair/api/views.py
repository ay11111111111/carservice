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
from datetime import time

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
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

def get_free_times(date, autoservice):
    appointments = Appointment.objects.filter(autoservice=autoservice, date=date)
    weekday = date.weekday() + 1
    openinghours = OpeningHours.objects.get(autoservice=autoservice, weekday=weekday)
    free_times = []
    booked_times = {}

    for appointment in appointments:
        t = "%d:00" % appointment.start_time.hour
        if t not in booked_times:
            booked_times.update({ t : autoservice.cars_per_timeslot-1})
        else:
            booked_times[t] -= 1

    for i in range(openinghours.worktime_from.hour, openinghours.worktime_till.hour):
        t = "%d:00" % i
        if i != openinghours.lunchtime_from.hour:
            if t not in booked_times or booked_times[t]>0:
                free_times.append(t)

    return free_times

class FreeSlotsView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FreeSlotsSerializer

    def get(self, request, pk, format=None):
        autoservice = AutoService.objects.get(pk=pk)
        datenow = datetime.date.today()
        data = []
        i, j = 0, 0
        while j != 4:
            date = datetime.date.today()+datetime.timedelta(days=i)
            weekday = date.weekday() + 1
            openinghours = OpeningHours.objects.get(autoservice=autoservice, weekday=weekday)
            if openinghours.working:
                times = get_free_times(date, autoservice)
                if len(times) != 0 :
                    data.append({"date":date, 'times':times})
                    j+=1
            i += 1

        return Response(data)


class AppointmentCreateView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentCreateSerializer

    def create(self, request, format=None):
        user = request.user
        appointment = Appointment(user=user)
        serializer = self.serializer_class(appointment, data=request.data)
        data = {}
        if serializer.is_valid():
            appointment = serializer.save()
            data['id'] = appointment.id
            data['response'] = 'successfully created new appointment'
            data['user'] = appointment.user.name_surname
            data['autoservice'] = appointment.autoservice.id
            data['date'] = appointment.date
            data['start_time'] = appointment.start_time
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
