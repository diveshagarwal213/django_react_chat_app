from django.urls import path

from . import views

urlpatterns = [
    # Products
    path("gen/phone_number/", views.VerifyPhoneNumberApiView.as_view()),
    path("auth/", views.OtpAuthView.as_view()),
]
