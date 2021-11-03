from django.db import models

class ClimateData(models.Model):

    temperature = models.CharField(max_length=6)
    humidity = models.CharField(max_length=6)
    time = models.DateTimeField(auto_now_add=True)