from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


def material_upload_path(instance, filename):
    return f"materials/{instance.owner_id}/{filename}"


class Material(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        CLASS = "class", "Class"
        PUBLIC = "public", "Public"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    pdf = models.FileField(upload_to=material_upload_path, validators=[FileExtensionValidator(["pdf"])])
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.PRIVATE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.UPLOADED)
    original_filename = models.CharField(max_length=255, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.title and self.original_filename:
            self.title = self.original_filename
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.original_filename or "Material"
