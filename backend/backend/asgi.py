"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
asgi_application  = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from application.urls import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)