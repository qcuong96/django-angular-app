from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from .v1.views.views import welcome

router = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/v1/", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include("src.v1.urls")),
    path(
        "openapi/",
        get_schema_view(
            title="Welcome Leonerdo Backend APIs!",
            description="API developers hoping to use our service",
        ),
        name="openapi-schema",
    ),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    # re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    re_path(r"^$", welcome),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'rest_framework.exceptions.server_error'