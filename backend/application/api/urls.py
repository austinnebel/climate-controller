from django.conf.urls import url
from django.urls import path, include
from .views import ClimateDataAPI

urlpatterns = [
    path('', ClimateDataAPI.as_view()),
]