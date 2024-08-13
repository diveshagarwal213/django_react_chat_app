# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from chat.services import GetGroupNames

User = get_user_model()


class NotificationConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.user = AnonymousUser()
        super().__init__(*args, **kwargs)

    def connect(self):
        print("Notification connect")
        user = self.scope["user"]
        if not user.is_authenticated:
            self.close()
            return

        self.user = user
        self.room_group_name = GetGroupNames.get_user_personal_group(user_id=user.id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        # Leave room group
        if hasattr(self, "room_group_name"):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )

    def receive_json(self, content, **kwargs):
        # message = content.get("message", None)
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type": "send_ws_notification", "text": message}
        # )
        pass

    def send_ws_notification(self, event):
        print("from:send_ws_notification", event)
        text = event["text"]
        # Send message to WebSocket
        self.send_json({"message": text})
