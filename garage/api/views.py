from ..models import Car, Event, CarModel, CarBrand, CalendarEvent, Fuel
from .serializers import *
from .filters import EventFilter, CalendarEventFilter
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
from django.db.models.query import Q

@swagger_auto_schema(method='get', operation_description="GET list of cars")
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def car_list(request):
    user = request.user
    cars = user.car_set
    serializer = CarSerializer(cars, many=True, context={"request": request})
    return Response(serializer.data)


@swagger_auto_schema(method='get', operation_description="GET list of car models by brand_id")
@api_view(['GET'])
def carmodel_list(request, pk):
    carbrand = CarBrand.objects.get(pk=pk)
    carmodels = carbrand.carmodel_set
    serializer = CarModelSerializer(carmodels, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get', operation_description="GET list of car models and brands")
@api_view(['GET'])
def carbrand_list(request):
    carbrands = CarBrand.objects.all()
    serializer = CarBrandSerializer(carbrands, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=CarCreateSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def car_create(request):
    user = request.user
    car = Car(user=user)
    if request.method == 'POST':
        serializer = CarCreateSerializer(car, data=request.data)
        data = {}
        if serializer.is_valid():
            car = serializer.save()
            data['id'] = car.id
            data['response'] = 'successfully registered new car'
            data['user'] = car.user.email
            data['car_marka'] = car.car_marka.name
            data['car_model'] = car.car_model.name
        else:
            data = serializer.errors

        return Response(data)


@swagger_auto_schema(method='put', request_body=CarSerializer)
@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def car_update(request, pk):

    try:
        car = Car.objects.get(pk=pk)
        user = request.user
        if user != car.user:
            return Response({'response':'You dont have a permission to update this car!'})

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['get', 'delete'])
@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def car_detail(request, pk):
    try:
        car = Car.objects.get(pk=pk)
        user = request.user
        if user != car.user:
            return Response({'response':'You dont have a permission to acess this car!'})

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CalendarEventView(viewsets.GenericViewSet):
    serializer_class = CalendarEventSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, format=None):
        user = request.user
        calendarevent = CalendarEvent(user=user)
        serializer = self.serializer_class(calendarevent, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_list(self, request, format=None):
        user = request.user
        calendarevents = CalendarEvent.objects.filter(car__user = user)
        serializer = self.serializer_class(calendarevents, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)


class EventView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_queryset(self):
        car = Car.objects.get(pk=self.kwargs['pk'])
        queryset = car.event_set
        queryset = queryset.filter(car__user=self.request.user)

        return queryset


class FuelView(ListAPIView):
    serializer_class = FuelSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Fuel.objects.all()

@swagger_auto_schema(method='post', request_body=ServiceEventSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def service_event_create(request, pk):
    car = Car.objects.get(pk=pk)
    event = Event(car=car,type='service')
    if request.method == 'POST':
        serializer = ServiceEventSerializer(event, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            car.probeg = serializer.data['probeg']
            car.save()
            data['response'] = 'successfully registered new service event'
        else:
            data = serializer.errors

        return Response(data)

@swagger_auto_schema(method='post', request_body=ServiceEventSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def other_event_create(request, pk):
    car = Car.objects.get(pk=pk)
    event = Event(car=car,type='other')
    if request.method == 'POST':
        serializer = ServiceEventSerializer(event, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            car.probeg = serializer.data['probeg']
            car.save()
            data['response'] = 'successfully registered new other event'
        else:
            data = serializer.errors

        return Response(data)

@swagger_auto_schema(method='post', request_body=ZapravkaEventSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def zapravka_event_create(request, pk):
    car = Car.objects.get(pk=pk)
    event = Event(car=car,type='zapravka')
    if request.method == 'POST':
        serializer = ZapravkaEventSerializer(event, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            current_amount_of_fuel = serializer.data['current_amount_of_fuel'] + serializer.data['amount_of_fuel']
            car.rashod_topliva = (current_amount_of_fuel - car.current_vol)//(serializer.data['probeg'] - car.probeg)
            car.probeg = serializer.data['probeg']
            car.current_vol = current_amount_of_fuel
            car.save()
            data['response'] = 'successfully registered new zapravka event'
        else:
            data = serializer.errors

        return Response(data)


@swagger_auto_schema(methods=['get', 'delete'], operation_description='GET or DELETE event by its id')
@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
        user = request.user
        if user != event.car.user:
            return Response({'response':'You dont have a permission to acess this car!'})

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(car)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyUploadView(viewsets.GenericViewSet):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CarImgSerializer
    # queryset = ''

    @swagger_auto_schema(method='post', operation_description='POST Image to the car')
    @action(detail=True, methods=['post',], parser_classes=(MultiPartParser,))
    def create(self, request, pk, format=None):
        car = Car.objects.get(pk=pk)
        img = CarImages(car=car)
        serializer = self.serializer_class(img, data=request.data, context={"request":request})

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', operation_description="GET list of fuels")
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def fuel_list(request):
    serializer = FuelChoiceSerializer()
    return Response(serializer.data)
