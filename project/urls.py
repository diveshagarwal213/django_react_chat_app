"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

# admin
admin.site.site_header = "Project C"
admin.site.index_title = "Admin Panel"

# swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Project C API's",
        default_version="v1",
        description="API Description",
        # terms_of_service="https://www.yourapp.com/terms/",
        # contact=openapi.Contact(email="contact@yourapp.com"),
        # license=openapi.License(name="Your License"),
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # lib urls
    path("api/auth/", include("djoser.urls.jwt")),
    # project apps urls
    path("api/otp/", include("otp.urls")),
    path("api/core/", include("core.urls")),
    # api docs & debug
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]
