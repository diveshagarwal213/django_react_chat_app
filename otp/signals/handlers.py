# from django.conf import settings
# from django.dispatch import receiver

# from otp.services import TwilioService
# from otp.signals import verify_phone_number_updated


# @receiver(verify_phone_number_updated)
# def on_verify_phone_number_updated(sender, **kwargs):
#     if settings.PROJECT_RUNNING_ENV != "prod":
#         return
#     twilio_payload = kwargs.get("twilio_payload")
#     # twilio client
#     try:
#         if twilio_payload is not None:
#             pass
#             twilio_service = TwilioService()
#             twilio_service.send_sms(**twilio_payload)
#             twilio_service.send_whats_app(**twilio_payload)
#     except Exception as e:
#         print(str(e))
