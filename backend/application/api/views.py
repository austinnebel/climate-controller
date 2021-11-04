
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from application.models import ClimateData
from application.serializers import ClimateDataSerializer

from datetime import datetime, timedelta

TIME_DURATION = timedelta(hours = 3)

class ClimateDataAPI(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def list(self, request, *args, **kwargs):
        """
        Lists all climate data entries.
        """
        duration = int(request.data.get("duration")) if request.data.get("duration") else TIME_DURATION

        queryset = ClimateData.objects.filter(time__gte=datetime.now() - duration).order_by('time')
        serializer = ClimateDataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Gets a single climate data entry.
        """
        queryset = ClimateData.objects.all()
        data = get_object_or_404(queryset, pk=pk)
        serializer = ClimateDataSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a climate data entry.
        """

        serializer = ClimateDataSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def createbatch(self, request, *args, **kwargs):
        """
        Creates a batch of climate data entries.
        """

        if not request.data.get('batch'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ClimateDataSerializer(data=request.data.get('batch'), many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def purge(self, request):
        """
        Removes old entries from the database.
        """
        expire_time = int(request.data.get("expire_time")) if request.data.get("expire_time") else TIME_DURATION

        queryset = ClimateData.objects.filter(time__lte=datetime.now() - expire_time)
        serializer = ClimateDataSerializer(queryset, many=True)

        for object in queryset:
            object.delete()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def purgeall(self, request):
        """
        Removes all entries from the database.
        """

        queryset = ClimateData.objects.all()
        serializer = ClimateDataSerializer(queryset, many=True)

        for object in queryset:
            object.delete()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Deletes a single climate data entry.
        """
        queryset = ClimateData.objects.all()
        data = get_object_or_404(queryset, pk=pk)
        data.delete()

        return Response(status=status.HTTP_200_OK)