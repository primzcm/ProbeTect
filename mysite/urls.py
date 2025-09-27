﻿from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("materials/", include(("materials.urls", "materials"), namespace="materials")),
    path("quizzes/", include(("quizzes.urls", "quizzes"), namespace="quizzes")),
    path("", include("blog.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
