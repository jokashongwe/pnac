from django.contrib import admin
from .models import GalleryImage

@admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'date_taken')
    list_filter = ('category',)
    
    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return ""