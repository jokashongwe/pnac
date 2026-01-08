from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_published')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    
    # Génération auto du slug basée sur le titre (dans la langue par défaut)
    prepopulated_fields = {'slug': ('title',)}