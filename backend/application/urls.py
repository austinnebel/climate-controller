"""
Defines Django REST API routes of the application.
"""
from django.conf.urls import url
from django.urls import path, include
from application.api.views import ClimateDataAPI, DeviceDataAPI
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from application.consumers import WebsocketConsumer


router = DefaultRouter()
router.register(r'data', ClimateDataAPI, basename='data')
router.register(r'device', DeviceDataAPI, basename='device')

"""
HTTP URL locations.
"""
urlpatterns = router.urls

"""
Websocket URL locations.
"""
websocket_urlpatterns = [
    # Route for the /ws/currentData/ websocket
    url(r"^ws/currentData/", WebsocketConsumer.as_asgi()),
]