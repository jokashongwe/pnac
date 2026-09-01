from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_utils import image_preview
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("image_preview", "title", "category", "date_taken")
    list_display_links = ("title",)
    list_filter = ("category", "date_taken")
    search_fields = ("title", "description")
    date_hierarchy = "date_taken"
    readonly_fields = ("image_preview_large",)
    fieldsets = (
        (_("Média"), {"fields": ("image_preview_large", "image", "title", "description")}),
        (_("Classement"), {"fields": ("category", "date_taken")}),
    )

    def image_preview(self, obj):
        return image_preview(obj.image)

    image_preview.short_description = _("Aperçu")

    def image_preview_large(self, obj):
        return image_preview(obj.image, size=180, radius=12)

    image_preview_large.short_description = _("Aperçu")
