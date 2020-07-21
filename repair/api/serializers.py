from rest_framework import serializers
from ..models import Service, AutoserviceType, CTO

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id','name')


class CTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = CTO
        fields = ('id', 'name', 'type', 'address', 'rating', 'image')
        depth=1



class ServiceIDSerializer(serializers.Serializer):
    ids = serializers.CharField(max_length=100, required=False)
