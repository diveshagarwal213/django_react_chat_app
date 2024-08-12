from django.urls import include, path
from rest_framework_nested import routers

from my_app import views

# router config
router = routers.DefaultRouter()

# Level One
router.register("interests", views.InterestViewSet, basename="interests")

urlpatterns = [path("", include(router.urls))]
