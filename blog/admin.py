from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from core.admin_utils import CKEditorAdminMixin, image_preview
from .models import Post


@admin.register(Post)
class PostAdmin(CKEditorAdminMixin, TranslationAdmin):
    group_fieldsets = True
    save_on_top = True
    date_hierarchy = "created_at"
    list_display = ("cover_preview", "title", "category", "author", "is_published", "created_at")
    list_display_links = ("title",)
    list_filter = ("category", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author",)
    list_per_page = 25
    fieldsets = (
        (_("Contenu"), {"fields": ("title", "slug", "excerpt", "content")}),
        (_("Mise en page"), {"fields": ("image", "category")}),
        (_("Publication"), {"fields": ("author", "is_published")}),
    )

    def cover_preview(self, obj):
        return image_preview(obj.image)

    cover_preview.short_description = _("Visuel")

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
