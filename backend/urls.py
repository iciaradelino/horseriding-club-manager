from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("members/", include("members.urls", namespace="members")),
    path("horses/", include("horses.urls", namespace="horses")),
    path("lessons/", include("lessons.urls", namespace="lessons")),
    path("staff/", include("staff.urls", namespace="staff")),
    path("billing/", include("billing.urls", namespace="billing")),
    path("", include("dashboard.urls", namespace="dashboard")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
