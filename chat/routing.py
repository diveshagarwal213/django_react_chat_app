# chat/routing.py
from channelsmultiplexer.demultiplexer import AsyncJsonWebsocketDemultiplexer
from django.urls import re_path

from chat import consumers

websocket_urlpatterns = [
    re_path(
        r"^ws/$",
        AsyncJsonWebsocketDemultiplexer.as_asgi(
            # chat_stream=consumers.ChatConsumer.as_asgi(),
            notification_stream=consumers.NotificationConsumer.as_asgi(),
        ),
    ),
]
