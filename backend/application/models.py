from django.db import models

class ClimateData(models.Model):
    temperature = models.FloatField(max_length=6)
    humidity = models.FloatField(max_length=6)
    time = models.TimeField(auto_now = True)
