from django.conf import settings
from twilio.rest import Client


class TwilioService:

    def __init__(self) -> None:
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_sms(self, to: str, body: str, from_=settings.TWILIO_FROM_NUMBER):
        return self.client.messages.create(to=to, body=body, from_=from_)

    def send_whats_app(
        self, to: str, body: str, from_=settings.TWILIO_FROM_WHATSAPP_NUMBER
    ):
        return self.client.messages.create(
            to=f"whatsapp:{to}", body=body, from_=f"whatsapp:{from_}"
        )
