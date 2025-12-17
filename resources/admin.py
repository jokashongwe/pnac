from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'extension', 'is_public', 'created_at')
    list_filter = ('category', 'is_public')
    search_fields = ('title', 'description')