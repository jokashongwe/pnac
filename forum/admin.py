from django.contrib import admin
from .models import Topic, Post

class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_post_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostInline] # Permet de voir les messages directement dans le sujet

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'topic', 'created_at')
    search_fields = ('content', 'visitor_name')
    list_filter = ('created_at', 'topic')