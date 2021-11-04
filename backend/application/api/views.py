
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from application.models import ClimateData
from application.serializers import ClimateDataSerializer

from datetime import datetime, timedelta

TIME_DURATION = timedelta(hours = 3)

class ClimateDataAPI(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request, *args, **kwargs):
        """
        Retrieves climate data entries.
        """
        data = ClimateData.objects.filter(time__gte=datetime.now() - TIME_DURATION)
        serializer = ClimateDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a climate data entry.
        """
        data = {
            'temperature': request.data.get('temperature'),
            'humidity': request.data.get('humidity'),
        }

        serializer = ClimateDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)