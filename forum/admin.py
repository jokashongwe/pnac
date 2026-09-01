from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post, Topic, TopicAccessRequest


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    readonly_fields = ("created_at",)
    fields = ("author", "visitor_name", "content", "created_at")
    show_change_link = True


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("title", "access_mode", "created_by", "get_post_count", "is_active", "created_at")
    list_filter = ("is_active", "access_mode", "created_at")
    list_editable = ("is_active",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("created_by", "author")
    inlines = [PostInline]
    fieldsets = (
        (_("Sujet"), {"fields": ("title", "slug", "description")}),
        (_("Accès"), {"fields": ("access_mode", "created_by", "author", "is_active")}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("display_name", "topic", "author", "created_at")
    search_fields = ("content", "visitor_name", "author__name")
    list_filter = ("created_at", "topic")
    autocomplete_fields = ("topic", "author")


@admin.register(TopicAccessRequest)
class TopicAccessRequestAdmin(admin.ModelAdmin):
    list_display = ("member", "topic", "status", "created_at", "reviewed_by", "reviewed_at")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("member__name", "topic__title")
    autocomplete_fields = ("member", "topic", "reviewed_by")
