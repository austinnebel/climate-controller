"""
Contains all database models for the application.
"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CheckConstraint, Q

class ClimateData(models.Model):
    """
    The database model for climate data. This includes temperature, humidity, and the time of recording.
    """
    temperature = models.FloatField(max_length=6, blank=False)
    humidity = models.FloatField(max_length=6, blank=False, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        constraints = (
            # validates humidity
            CheckConstraint(
                check=Q(humidity__gte=0.0) & Q(humidity__lte=100.0),
                name='%(class)s_humidity_range'),
            )

class DeviceData(models.Model):
    """
    The database model for device data. This includes the event that happened and the time of recording.
    """
    device = models.CharField(max_length=12, blank=False)
    event = models.CharField(max_length=12, blank=False)
    time = models.DateTimeField(auto_now_add=True, blank=True)