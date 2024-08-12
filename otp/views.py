# from django.shortcuts import render
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from otp.models import VerifyPhoneNumber
from otp.signals import verify_phone_number_updated

from .serializers import (
    OtpAuthResponseSerializer,
    OtpAuthSerializer,
    VerifyPhoneNumberSerializer,
)

User = get_user_model()


class VerifyPhoneNumberApiView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyPhoneNumberSerializer,
        responses={200: "raw_otp"},
        operation_description="Custom operation description here",
    )
    def post(self, req):
        raw_otp = str(random.randint(1000, 9999))
        serializer = VerifyPhoneNumberSerializer(
            data=req.data, context={"raw_otp": raw_otp}
        )
        serializer.is_valid(raise_exception=True)
        otp_for = serializer.validated_data.get("otp_for")
        serializer.save()
        message = None
        if otp_for == VerifyPhoneNumber.OTP_AUTH_LOGIN_REGISTER:
            message = f"{raw_otp} is your verification code for citykeiks.com"

        # return raw otp if dev env
        if settings.PROJECT_RUNNING_ENV == "dev":
            return Response(
                {"raw_otp": raw_otp, "status": "Ok"}, status=status.HTTP_201_CREATED
            )

        twilio_payload = {
            "body": message,
            "to": serializer.validated_data.get("phone_number"),
        }
        # sending signal
        verify_phone_number_updated.send(
            sender=self.__class__, twilio_payload=twilio_payload
        )
        return Response({"status": "Ok"}, status=status.HTTP_201_CREATED)


class OtpAuthView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=OtpAuthSerializer,
        responses={200: OtpAuthResponseSerializer},
        operation_description="OTP Login/Register",
    )
    def post(self, req):
        serializer = OtpAuthSerializer(
            data=req.data,
        )
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone_number")
        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            user = User.objects.create(phone_number=phone_number)

        # create token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=status.HTTP_200_OK,
        )
