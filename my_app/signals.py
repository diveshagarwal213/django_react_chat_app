from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from chat.services import WebSocketNotificationService
from my_app.models import ChatMessage, Interest


@receiver(post_save, sender=Interest)
def interest_post_save(sender, instance: Interest, created, **kwargs):
    user_id = instance.sent_by_id
    user_id_2 = instance.sent_to_id
    web_socket_notification_service = WebSocketNotificationService()
    web_socket_notification_service.send_notification(user_id=user_id)
    web_socket_notification_service.send_notification(user_id=user_id_2)


# delete
@receiver(post_delete, sender=Interest)
def interest_post_delete(sender, instance: Interest, **kwargs):
    user_id = instance.sent_by_id
    user_id_2 = instance.sent_to_id
    web_socket_notification_service = WebSocketNotificationService()
    web_socket_notification_service.send_notification(user_id=user_id)
    web_socket_notification_service.send_notification(user_id=user_id_2)


@receiver(post_save, sender=ChatMessage)
def chat_message_post_save(sender, instance: ChatMessage, **kwargs):
    web_socket_notification_service = WebSocketNotificationService()
    # instance.user_id ==> creator of the message
    if instance.interest.sent_to.id == instance.user_id:
        web_socket_notification_service.send_notification(
            user_id=instance.interest.sent_by.id, text="UPDATE_CHAT"
        )
    else:
        web_socket_notification_service.send_notification(
            user_id=instance.interest.sent_to.id, text="UPDATE_CHAT"
        )
