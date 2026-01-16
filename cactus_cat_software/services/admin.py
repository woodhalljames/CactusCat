from django.contrib import admin
from django.utils.html import format_html

from .models import ServiceCategory, ServicePackage


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "display_order", "package_count", "is_active"]
    list_editable = ["display_order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]

    def package_count(self, obj):
        return obj.packages.count()

    package_count.short_description = "Packages"


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price_display",
        "is_active",
        "display_order",
        "created",
    ]
    list_filter = ["category", "is_active", "created"]
    list_editable = ["is_active", "display_order"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description", "short_description"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("name", "slug", "category", "short_description"),
            },
        ),
        (
            "Details",
            {
                "fields": ("features", "description", "image"),
            },
        ),
        (
            "Pricing & Timeline",
            {
                "fields": (
                    "price",
                    "is_price_starting_from",
                    "estimated_delivery_days",
                ),
            },
        ),
        (
            "Display",
            {
                "fields": ("is_active", "display_order"),
            },
        ),
    )

    def price_display(self, obj):
        if obj.is_price_starting_from:
            return format_html("Starting from <strong>${}</strong>", obj.price)
        return format_html("<strong>${}</strong>", obj.price)

    price_display.short_description = "Price"
