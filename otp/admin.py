from django.contrib import admin
from django.http.request import HttpRequest

from .models import VerifyPhoneNumber


# Register your models here.
@admin.register(VerifyPhoneNumber)
class VerifyPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "otp_for", "expire_at"]
    # readonly_fields = ["phone_number", "otp", "otp_for", "expire_at"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False
