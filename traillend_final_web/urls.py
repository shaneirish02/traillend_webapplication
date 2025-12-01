from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from core.views import run_smart_scheduler

urlpatterns = [
    path("admin/", admin.site.urls),

    # CORRECTED: must have trailing slash
    path("api/", include("core.urls")),

    # Scheduler endpoint
    path("api/run-scheduler/", run_smart_scheduler),

    # Redirect root → login page
    path("", lambda request: redirect("login")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
