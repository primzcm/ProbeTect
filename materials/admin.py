from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "visibility", "status", "file_size", "created_at")
    list_filter = ("visibility", "status", "created_at")
    search_fields = ("title", "subject", "owner__username", "storage_path")
    readonly_fields = ("created_at", "updated_at", "storage_path", "public_url", "file_size", "content_type")
    fieldsets = (
        (None, {"fields": ("owner", "title", "subject", "description", "visibility", "status")}),
        ("File", {"fields": ("original_filename", "storage_path", "public_url", "file_size", "content_type")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
