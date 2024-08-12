from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    actions = ["gen_tokens"]
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "email", "first_name", "last_name", "is_staff")
    search_fields = ("phone_number", "first_name", "last_name", "email")
    ordering = ()

    @admin.action(description="Generate JWT TOKENS")
    def gen_tokens(self, request: HttpRequest, queryset: QuerySet[Any]):
        user = queryset.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        self.message_user(
            request,
            f"refresh_token {user}: {refresh_token} \n \n Access:Token {access_token}",
        )
