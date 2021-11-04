from django.conf.urls import url
from django.urls import path, include

from django.conf.urls import url
from django.urls import path, include
from application.api.views import ClimateDataAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api', ClimateDataAPI, basename='api')
urlpatterns = router.urls
