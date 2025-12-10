from django.contrib import admin
from .models import TeamMember
from django.utils.html import format_html

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'role', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'role')
    list_editable = ('order',) # Permet de réorganiser l'ordre directement depuis la liste

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />', obj.photo.url)
        return "Pas de photo"
    photo_preview.short_description = "Photo"