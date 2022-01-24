from channels.routing import URLRouter
from django.urls import path
from yobaclub.logic.sockets.cinema_chat import CinemaChatSocket

websockets = URLRouter([
    path("socket/cinema/<str:room_id>", CinemaChatSocket.as_asgi(), name="Cinema Chat WebSocket")
])