from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from django.urls import (
    include,
    path,
)
admin.site.site_header = (
    "School Platform Admin"
)

admin.site.site_title = (
    "School Platform"
)

admin.site.index_title = (
    "Administration"
)

urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("apps.dashboard.urls"),
    ),
    path(
    "accounts/",
    include("apps.accounts.urls"),
),
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
    path(
    "attendance/",
    include("apps.attendance.urls"),
),
    path(
    "payments/",
    include("apps.payments.urls"),
),
path(
    "rankings/",
    include("apps.rankings.urls"),
),
path(
    "classes/",
    include("apps.classes.urls"),
),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )