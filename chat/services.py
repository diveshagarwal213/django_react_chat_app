from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class GetGroupNames:
    @staticmethod
    def get_user_personal_group(user_id):
        return f"user-{user_id}"

    @staticmethod
    def get_chat_group(room_name):
        return f"chat-{room_name}"


class WebSocketNotificationService:
    def __init__(self) -> None:
        self.channel_layer = get_channel_layer()

        # event_types
        self.event_type_send_ws_notification = "send_ws_notification"

    def send_notification(self, user_id, text="UPDATE_INTEREST"):
        group_name = GetGroupNames.get_user_personal_group(user_id=user_id)
        event = {
            "type": self.event_type_send_ws_notification,
            "text": text,
        }
        async_to_sync(self.channel_layer.group_send)(group_name, event)
