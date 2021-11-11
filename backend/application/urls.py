from django.conf.urls import url
from django.urls import path, include
from application.api.views import ClimateDataAPI, DeviceDataAPI
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'data', ClimateDataAPI, basename='data')
router.register(r'device', DeviceDataAPI, basename='device')

urlpatterns = router.urls
