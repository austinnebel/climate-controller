from django.urls import re_path
from django.conf.urls import url

from application.consumers import DataConsumer

websocket_urlpatterns = [
    # We use re_path() due to limitations in URLRouter.
    # translates to absolute ws/data
    url(r"^ws/currentData/", DataConsumer.as_asgi()),
]