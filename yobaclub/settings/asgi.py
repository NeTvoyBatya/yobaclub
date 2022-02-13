import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, get_default_application
from channels.auth import AuthMiddlewareStack
from yobaclub.websockets import websockets
from django import setup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yobaclub.settings.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(websockets)
    }
)