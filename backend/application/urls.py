from django.conf.urls import url
from django.urls import path, include

from django.conf.urls import url
from django.urls import path, include
from application.api.views import ClimateDataAPI, DeviveDataAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'data', ClimateDataAPI, basename='data')
router.register(r'device', DeviveDataAPI, basename='device')
urlpatterns = router.urls
