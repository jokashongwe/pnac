from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from team.models import PhoneOTP, TeamMember, VolunteerApplication
from team.services.accounts import provision_member_access
from core.admin_utils import CKEditorAdminMixin


class TeamMemberAdminForm(forms.ModelForm):
    access_password = forms.CharField(
        label=_("Mot de passe de l'espace"),
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text=_("Renseignez un mot de passe pour créer ou réinitialiser l'accès membre."),
    )

    class Meta:
        model = TeamMember
        fields = "__all__"


@admin.register(TeamMember)
class TeamMemberAdmin(CKEditorAdminMixin, TranslationAdmin):
    group_fieldsets = True
    save_on_top = True
    form = TeamMemberAdminForm
    list_display = (
        "photo_preview",
        "name",
        "role",
        "category",
        "email",
        "phone",
        "has_access",
        "phone_verified",
        "is_forum_banned",
        "order",
    )
    list_filter = ("category", "phone_verified", "is_forum_banned")
    search_fields = ("name", "role", "email", "phone")
    list_editable = ("order",)
    readonly_fields = ("user",)
    fieldsets = (
        (
            None,
            {"fields": ("name", "role", "category", "bio", "photo", "order")},
        ),
        (_("Contact"), {"fields": ("email", "phone")}),
        (
            _("Espace membre"),
            {
                "fields": (
                    "user",
                    "access_password",
                    "phone_verified",
                    "is_forum_banned",
                )
            },
        ),
        (_("Réseaux"), {"fields": ("facebook_url", "linkedin_url", "twitter_url")}),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.photo.url,
            )
        return _("Pas de photo")

    photo_preview.short_description = _("Photo")

    def has_access(self, obj):
        return obj.has_login()

    has_access.boolean = True
    has_access.short_description = _("Accès")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        password = form.cleaned_data.get("access_password")
        if password:
            try:
                provision_member_access(obj, password)
                self.message_user(
                    request,
                    _("L'espace membre a été créé ou le mot de passe a été mis à jour."),
                    messages.SUCCESS,
                )
            except ValueError as exc:
                self.message_user(request, str(exc), messages.ERROR)


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("full_name", "email", "phone", "preferred_notification", "status", "created_at")
    list_filter = ("status", "preferred_notification")
    search_fields = ("full_name", "email", "phone")
    readonly_fields = ("created_at",)
    actions = ["approve_applications", "reject_applications"]

    def approve_applications(self, request, queryset):
        queryset.update(status="APPROVED")

    approve_applications.short_description = _("Approuver les candidatures sélectionnées")

    def reject_applications(self, request, queryset):
        queryset.update(status="REJECTED")

    reject_applications.short_description = _("Rejeter les candidatures sélectionnées")


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ("member", "created_at", "expires_at", "attempts", "used_at")
    list_filter = ("used_at",)
    search_fields = ("member__name", "member__phone")
    readonly_fields = ("member", "code_hash", "created_at", "expires_at", "attempts", "used_at")
