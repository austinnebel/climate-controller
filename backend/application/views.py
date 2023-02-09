"""
Defines all Django Views.
"""
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from application.serializers import UserSerializer, GroupSerializer, ClimateDataSerializer
from application.models import ClimateData


class UserViewSet(viewsets.ModelViewSet):
    """
    All application users.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]


class GroupViewSet(viewsets.ModelViewSet):
    """
    All user groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

class ClimateDataViewSet(viewsets.ModelViewSet):
    """
    All climate data posted from the embedded device.
    """
    queryset = ClimateData.objects.all()
    serializer_class = ClimateDataSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]
