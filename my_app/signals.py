from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from chat.services import WebSocketNotificationService
from my_app.models import Interest


# UPDATE
@receiver(post_save, sender=Interest)
def interest_post_save(sender, instance: Interest, created, **kwargs):
    user_id = instance.sent_by_id
    user_id_2 = instance.sent_to_id
    web_socket_notification_service = WebSocketNotificationService()
    web_socket_notification_service.send_update_interest_notification(user_id=user_id)
    web_socket_notification_service.send_update_interest_notification(user_id=user_id_2)


# delete
@receiver(post_delete, sender=Interest)
def interest_post_delete(sender, instance: Interest, **kwargs):
    user_id = instance.sent_by_id
    user_id_2 = instance.sent_to_id
    web_socket_notification_service = WebSocketNotificationService()
    web_socket_notification_service.send_update_interest_notification(user_id=user_id)
    web_socket_notification_service.send_update_interest_notification(user_id=user_id_2)
