from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CheckConstraint, Q

class ClimateData(models.Model):
    temperature = models.FloatField(max_length=6, blank=False)
    humidity = models.FloatField(max_length=6, blank=False, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        constraints = (
            # validates humidity
            CheckConstraint(
                check=Q(humidity__gte=0.0) & Q(humidity__lte=100.0),
                name='humidity_range'),
            )