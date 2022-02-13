import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from yobaclub.websockets import websockets


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yobaclub.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(websockets)
    }
)