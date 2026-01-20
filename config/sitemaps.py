"""Sitemap configuration for Cactus Cat Software."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from cactus_cat_software.blog.models import BlogPost
from cactus_cat_software.services.models import ServicePackage


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""

    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ["home", "about", "contact"]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    """Sitemap for blog posts."""

    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(status="published").order_by("-published_date")

    def lastmod(self, obj):
        return obj.modified

    def location(self, obj):
        return obj.get_absolute_url()


class ServicesSitemap(Sitemap):
    """Sitemap for service packages."""

    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return ServicePackage.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.modified

    def location(self, obj):
        return obj.get_absolute_url()


class ServicesCatalogSitemap(Sitemap):
    """Sitemap for the services catalog page."""

    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return ["services:catalog"]

    def location(self, item):
        return reverse(item)


sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
    "services": ServicesSitemap,
    "services-catalog": ServicesCatalogSitemap,
}
