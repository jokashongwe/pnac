from django.contrib import admin

from .models import Post, Topic, TopicAccessRequest


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "access_mode", "created_by", "get_post_count", "is_active", "created_at")
    list_filter = ("is_active", "access_mode", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PostInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("display_name", "topic", "author", "created_at")
    search_fields = ("content", "visitor_name", "author__name")
    list_filter = ("created_at", "topic")


@admin.register(TopicAccessRequest)
class TopicAccessRequestAdmin(admin.ModelAdmin):
    list_display = ("member", "topic", "status", "created_at", "reviewed_by", "reviewed_at")
    list_filter = ("status", "created_at")
    search_fields = ("member__name", "topic__title")
