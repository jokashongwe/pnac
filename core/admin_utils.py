from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget


CMS_EDITOR_FIELDS = {
    "content": "cms",
    "content_fr": "cms",
    "content_en": "cms",
    "description": "cms",
    "description_fr": "cms",
    "description_en": "cms",
    "bio": "default",
    "bio_fr": "default",
    "bio_en": "default",
}


class CKEditorAdminMixin:
    """Attaches CKEditor 5 to translated TextFields in the admin."""

    ckeditor_fields = CMS_EDITOR_FIELDS

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        config_name = self.ckeditor_fields.get(db_field.name)
        if field is not None and config_name:
            field.widget = CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name=config_name,
            )
        return field


def image_preview(image_field, size=52, radius=8):
    if image_field:
        return format_html(
            '<img src="{}" alt="" style="width:{}px;height:{}px;object-fit:cover;border-radius:{}px;background:#ecfdf5;" />',
            image_field.url,
            size,
            size,
            radius,
        )
    return format_html('<span style="color:#9ca3af;">{}</span>', _("Aucune image"))
