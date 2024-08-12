from django.contrib.auth.hashers import check_password
from django.utils import timezone
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from core.models import User
from otp.models import VerifyPhoneNumber


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "phone_number",
            "password",
            "email",
            "first_name",
            "last_name",
            "otp",
        ]

    otp = serializers.CharField(max_length=4, write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp")
        phone_number = attrs.get("phone_number")
        try:
            verify_phone_number_obj = VerifyPhoneNumber.objects.get(
                phone_number=phone_number,
                otp_for=VerifyPhoneNumber.OTP_NEW_ACCOUNT,
                expire_at__gt=timezone.now(),
            )

            if not check_password(otp, verify_phone_number_obj.otp):
                raise serializers.ValidationError({"otp": "otp expire"})

            verify_phone_number_obj.delete()

            return attrs
        except Exception as exc:
            raise serializers.ValidationError({"otp": "otp expire"}) from exc

    def create(self, validated_data):
        validated_data.pop("otp")
        return User.objects.create_user(**validated_data)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "phone_number",
            "email",
            "first_name",
            "last_name",
        ]
        ref_name = "custom-user-serializer"
