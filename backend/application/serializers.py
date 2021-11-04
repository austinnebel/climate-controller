from django.contrib.auth.models import User, Group
from rest_framework import serializers
from application.models import ClimateData

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClimateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateData
        fields = ['id', 'temperature', 'humidity', 'time']