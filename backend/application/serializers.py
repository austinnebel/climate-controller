from django.contrib.auth.models import User, Group
from rest_framework import serializers
from application.models import ClimateData, DeviceData

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for `User` models.
    """
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for `Group` models.
    """
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClimateDataSerializer(serializers.ModelSerializer):
    """
    Serializer for `ClimateData` models.
    """
    class Meta:
        model = ClimateData
        fields = ['id', 'temperature', 'humidity', 'time']

class DeviceDataSerializer(serializers.ModelSerializer):
    """
    Serializer for `DeviceData` models.
    """
    class Meta:
        model = DeviceData
        fields = ['id', 'device', 'event', 'time']