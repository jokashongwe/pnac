from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_utils import image_preview
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("cover_preview", "title", "category", "extension", "is_public", "created_at")
    list_display_links = ("title",)
    list_filter = ("category", "is_public")
    list_editable = ("is_public",)
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    fieldsets = (
        (_("Document"), {"fields": ("title", "description", "file", "cover_image")}),
        (_("Publication"), {"fields": ("category", "is_public")}),
    )

    def cover_preview(self, obj):
        return image_preview(obj.cover_image)

    cover_preview.short_description = _("Couverture")
