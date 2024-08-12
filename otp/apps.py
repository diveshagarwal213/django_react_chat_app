from django.apps import AppConfig


class OtpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "otp"

    def ready(self) -> None:
        import otp.signals.handlers  # noqa
