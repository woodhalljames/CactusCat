from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class BlogPost(TimeStampedModel):
    """Blog posts created via admin with Summernote editor."""

    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("published", _("Published")),
    ]

    # Basic Info
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="blog_posts",
        verbose_name=_("Author"),
    )

    # Content
    excerpt = models.TextField(
        _("Excerpt"),
        max_length=500,
        help_text="Short description for previews",
    )
    content = models.TextField(_("Content"))  # Summernote field

    # Media
    featured_image = models.ImageField(
        _("Featured Image"),
        upload_to="blog/",
        blank=True,
    )

    # Publishing
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )
    published_date = models.DateTimeField(
        _("Published Date"),
        null=True,
        blank=True,
    )

    # SEO
    meta_description = models.CharField(
        _("Meta Description"),
        max_length=160,
        blank=True,
    )

    # Display
    featured = models.BooleanField(
        _("Featured Post"),
        default=False,
        help_text="Show on homepage",
    )

    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ["-published_date", "-created"]
        indexes = [
            models.Index(fields=["-published_date", "status"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
