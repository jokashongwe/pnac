from django.contrib import admin
from .models import TeamMember, VolunteerApplication
from django.utils.html import format_html

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'role', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'role')
    list_editable = ('order',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />', obj.photo.url)
        return "Pas de photo"
    photo_preview.short_description = "Photo"

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'preferred_notification', 'status', 'created_at')
    list_filter = ('status', 'preferred_notification')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at',)
    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_applications.short_description = "Approuver les candidatures sélectionnées"

    def reject_applications(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_applications.short_description = "Rejeter les candidatures sélectionnées"