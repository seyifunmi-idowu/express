from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from authentication.views import fele_express_api
from helpers.utils import BothHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="Fele Express API",
        default_version="v1",
        description="API for Fele Express",
        terms_of_service="https://www.feleexpress.com/",
        contact=openapi.Contact(email="support@feleexpress.com"),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", fele_express_api, name="fele_express_api"),
    path("admin/", admin.site.urls),
    path("business/", include("business.urls")),
    path(
        "api/docs",
        login_required(schema_view.with_ui("swagger", cache_timeout=0)),
        name="doc-ui",
    ),
    path("api/v1/", include("authentication.urls")),
    path("api/v1/", include("customer.urls")),
    path("api/v1/", include("notification.urls")),
    path("api/v1/", include("order.urls")),
    path("api/v1/", include("rider.urls")),
    path("api/v1/", include("wallet.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Fele Express Admin"
admin.site.site_title = "Fele Express Admin | Deliver your package faster"
admin.site.index_title = "Welcome to Fele Express Admin"
