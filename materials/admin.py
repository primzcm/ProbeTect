from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "visibility", "status", "created_at")
    list_filter = ("visibility", "status", "created_at")
    search_fields = ("title", "subject", "owner__username")
    readonly_fields = ("created_at", "updated_at")
