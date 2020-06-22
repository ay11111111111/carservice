from ..models import Car, Event
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated


@swagger_auto_schema(method='get')
@api_view(['GET'])
def car_list(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=CarSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def car_create(request):
    user = request.user
    car = Car(user=user)
    if request.method == 'POST':
        serializer = CarSerializer(car, data=request.data)
        data = {}
        if serializer.is_valid():
            car = serializer.save()
            data['id'] = car.id
            data['response'] = 'successfully registered new car'
            data['user'] = car.user.email
            data['car_marka'] = car.car_model
            data['car_model'] = car.car_model
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

    except car.DoesNotExist:
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

    except car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            data['response'] = 'successfully registered new zapravka event'
        else:
            data = serializer.errors

        return Response(data)
