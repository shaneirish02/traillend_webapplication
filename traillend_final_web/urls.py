from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from core.views import run_smart_scheduler
from core.views import fix_images
from core.views import api_login



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", api_login),
    path("api/", include("core.urls")),

    # Scheduler endpoint
    path("api/run-scheduler/", run_smart_scheduler),

    path("fix-images/", fix_images),

    # Redirect root → login page
    path("", lambda request: redirect("login")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
