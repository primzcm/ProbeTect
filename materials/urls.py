from django.urls import path

from .views import MaterialUploadView

app_name = "materials"

urlpatterns = [
    path("upload/", MaterialUploadView.as_view(), name="upload"),
]
