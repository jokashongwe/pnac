from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from core.admin_utils import CKEditorAdminMixin, image_preview
from .models import Seminar, SeminarRegistration


class RegistrationInline(admin.TabularInline):
    model = SeminarRegistration
    extra = 0
    readonly_fields = ("total_amount", "payment_status", "reference")
    can_delete = False
    show_change_link = True


@admin.register(Seminar)
class SeminarAdmin(CKEditorAdminMixin, TranslationAdmin):
    group_fieldsets = True
    save_on_top = True
    list_display = ("cover_preview", "title", "start_date", "location", "registration_fee", "is_active")
    list_display_links = ("title",)
    list_editable = ("is_active",)
    search_fields = ("title", "location", "description")
    inlines = [RegistrationInline]
    fieldsets = (
        ("Contenu", {"fields": ("title", "description", "image")}),
        ("Logistique", {"fields": ("start_date", "end_date", "location")}),
        ("Tarifs", {"fields": ("registration_fee", "accommodation_fee")}),
        ("Publication", {"fields": ("is_active",)}),
    )

    def cover_preview(self, obj):
        return image_preview(obj.image)

    cover_preview.short_description = "Visuel"


@admin.register(SeminarRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "seminar", "participant_type", "origin", "total_amount", "payment_status")
    list_filter = ("seminar", "payment_status", "origin", "needs_accommodation")
    search_fields = ("full_name", "email", "reference")
    autocomplete_fields = ("seminar",)
