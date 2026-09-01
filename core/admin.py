from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from core.admin_utils import image_preview
from .models import CarouselItem


@admin.register(CarouselItem)
class CarouselItemAdmin(TranslationAdmin):
    group_fieldsets = True
    save_on_top = True
    list_display = ("cover_preview", "title", "order", "is_active")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    search_fields = ("title", "subtitle")
    fieldsets = (
        ("Contenu du slide", {"fields": ("title", "subtitle", "image")}),
        ("Bouton d'action", {"fields": ("button_text", "button_link")}),
        ("Publication", {"fields": ("order", "is_active")}),
    )

    def cover_preview(self, obj):
        return image_preview(obj.image, size=64, radius=10)

    cover_preview.short_description = "Visuel"
