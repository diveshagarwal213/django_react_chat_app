from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager


# Create your models here.
class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(unique=True)

    email = models.EmailField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return str(self.phone_number)

    class Meta:
        indexes = [
            models.Index(fields=["phone_number"]),
        ]
