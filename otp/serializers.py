from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from .models import VerifyPhoneNumber

User = get_user_model()


class VerifyPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyPhoneNumber
        fields = ["phone_number", "otp_for"]

    def validate(self, attrs):
        otp_for = attrs.get("otp_for")
        phone_number = attrs.get("phone_number")
        if otp_for == VerifyPhoneNumber.OTP_NEW_ACCOUNT:
            is_user_exist = User.objects.filter(phone_number=phone_number).exists()
            if is_user_exist:
                raise serializers.ValidationError(
                    {"phone_number": "user with this phone number already exists."}
                )

        # if last otp expired then only create
        verify_phone_number_obj = VerifyPhoneNumber.objects.filter(
            phone_number=phone_number,
            otp_for=otp_for,
            expire_at__gt=timezone.now(),
        ).first()
        if verify_phone_number_obj:
            remaining_seconds = verify_phone_number_obj.expire_at - timezone.now()
            raise serializers.ValidationError(
                ["NOT_EXPIRED", round(remaining_seconds.total_seconds())]
            )
        return super().validate(attrs)

    def save(self, **kwargs):
        self.is_valid(raise_exception=True)

        phone_number = self.validated_data.get("phone_number")
        otp_for = self.validated_data.get("otp_for")

        raw_otp = self.context.get("raw_otp")

        hashed_otp = make_password(raw_otp)

        expire_time = timezone.now() + timedelta(minutes=2)

        try:  # update
            verify_phone_number_item = VerifyPhoneNumber.objects.get(
                phone_number=phone_number
            )
            verify_phone_number_item.otp = hashed_otp
            verify_phone_number_item.expire_at = expire_time
            verify_phone_number_item.otp_for = otp_for
            verify_phone_number_item.save()
            self.instance = verify_phone_number_item
        except VerifyPhoneNumber.DoesNotExist:
            # add
            self.instance = VerifyPhoneNumber.objects.create(
                phone_number=phone_number,
                otp=hashed_otp,
                expire_at=expire_time,
                otp_for=otp_for,
            )

        return self.instance


class OtpAuthSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    otp = serializers.IntegerField()

    def validate(self, attrs: dict):
        phone_number = attrs.get("phone_number")
        otp = attrs.get("otp")
        try:
            verify_phone_number_obj = VerifyPhoneNumber.objects.get(
                phone_number=phone_number,
                otp_for=VerifyPhoneNumber.OTP_AUTH_LOGIN_REGISTER,
                expire_at__gt=timezone.now(),
            )

            if not check_password(otp, verify_phone_number_obj.otp):
                raise serializers.ValidationError({"otp": "otp expire"})

            verify_phone_number_obj.delete()

            return super().validate(attrs)

        except VerifyPhoneNumber.DoesNotExist as e:
            raise serializers.ValidationError({"otp": "otp expired"}) from e


class OtpAuthResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
