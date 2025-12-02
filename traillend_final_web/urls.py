from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from core.views import run_smart_scheduler, api_login

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API routes
    path("api/login/", api_login),
    path("api/run-scheduler/", run_smart_scheduler),

    # Main app URLs
    path("", include("core.urls")),     # <-- Must be BEFORE redirect root

    # Redirect ONLY root /
    path("", lambda request: redirect("/login/")),
]

# Serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
