from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from core.views import run_smart_scheduler, fix_images, api_login

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔥 Main API endpoints (RESTORE ORIGINAL)
    path("", include("core.urls")),

    # 🔥 Direct login API (optional, since it's also in core.urls)
    path("api/login/", api_login),

    # 🔥 Scheduler endpoint
    path("api/run-scheduler/", run_smart_scheduler),

    # Temporary image fixer
    path("fix-images/", fix_images),

    # Root redirect
    path("", lambda request: redirect("login")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
