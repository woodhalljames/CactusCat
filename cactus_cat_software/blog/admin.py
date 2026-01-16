from django.contrib import admin
from django.utils import timezone
from django_summernote.admin import SummernoteModelAdmin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    """Simple admin interface for blog posts."""

    # Simple list view
    list_display = ["title", "status", "featured", "published_date"]
    list_filter = ["status", "featured"]
    search_fields = ["title", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}

    # Rich text editor
    summernote_fields = ("content",)

    # Simple single-page form
    fields = [
        "title",
        "slug",
        "excerpt",
        "content",
        "featured_image",
        "status",
        "featured",
        "meta_description",
    ]

    def save_model(self, request, obj, form, change):
        # Auto-set author if not set
        if not obj.author:
            obj.author = request.user

        # Auto-set published date when status changes to published
        if obj.status == "published" and not obj.published_date:
            obj.published_date = timezone.now()

        super().save_model(request, obj, form, change)
