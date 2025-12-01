from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from core.views import run_smart_scheduler, api_login

urlpatterns = [
    # Redirect ONLY the exact root URL "/"
    path("", lambda request: redirect("/login/")),

    # Admin
    path("admin/", admin.site.urls),

    # Main app URLs
    path("", include("core.urls")),

    # Direct login API
    path("api/login/", api_login),

    # Scheduler endpoint
    path("api/run-scheduler/", run_smart_scheduler),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
