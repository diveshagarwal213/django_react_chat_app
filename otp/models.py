from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class VerifyPhoneNumber(models.Model):
    phone_number = PhoneNumberField()

    otp = models.TextField()

    OTP_NEW_ACCOUNT = "N"
    OTP_AUTH_LOGIN_REGISTER = "A"
    OTP_CHOICES = [
        (OTP_NEW_ACCOUNT, "New Account"),
        (OTP_AUTH_LOGIN_REGISTER, "Auth Login/Register"),
    ]
    otp_for = models.CharField(max_length=1, choices=OTP_CHOICES)

    expire_at = models.DateTimeField()
