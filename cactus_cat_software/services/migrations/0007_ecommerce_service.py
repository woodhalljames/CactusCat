from django.db import migrations


def add_ecommerce(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    try:
        category = ServiceCategory.objects.get(slug="custom-software-development")
    except ServiceCategory.DoesNotExist:
        return

    ServicePackage.objects.update_or_create(
        slug="ecommerce-store-build",
        defaults={
            "name": "Custom E-Commerce Store",
            "category": category,
            "short_description": "A fully custom online store built on a stack you own, with no platform fees, no transaction cuts, and no monthly Shopify bill eating your margin.",
            "features": (
                "Custom Django storefront with no SaaS platform dependency\n"
                "Product catalogue, variants, and inventory management\n"
                "Stripe Checkout integration for one-time and subscription products\n"
                "Order management dashboard with fulfilment tracking\n"
                "Customer accounts, order history, and email receipts\n"
                "Discount codes and promotional pricing engine\n"
                "SEO-optimised product pages out of the box\n"
                "Full source code and documentation delivered"
            ),
            "who_its_for": (
                "Product businesses paying monthly Shopify or Wix fees\n"
                "Founders launching a store who want to own the platform outright\n"
                "Businesses with non-standard product types that page-builders can't handle"
            ),
            "description": (
                "Shopify charges you monthly. Then per transaction. Then for every app you need. "
                "Ten years in, you've spent six figures and you still don't own anything. "
                "We build custom e-commerce stores on Django, a production-grade stack with no platform fees, "
                "no revenue share, and no lock-in. "
                "Product catalogue, Stripe payments, order management, customer accounts, and discount logic "
                "are all included as standard. "
                "You own the codebase outright from day one and host it on infrastructure you control. "
                "The store is yours, not rented."
            ),
            "price": "8500.00",
            "setup_fee": "2800.00",
            "monthly_price": "650.00",
            "is_price_starting_from": True,
            "display_order": 3,
            "estimated_delivery_days": 42,
            "is_active": True,
        },
    )


def remove_ecommerce(apps, schema_editor):
    ServicePackage = apps.get_model("services", "ServicePackage")
    ServicePackage.objects.filter(slug="ecommerce-store-build").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0006_seed_service_packages"),
    ]

    operations = [
        migrations.RunPython(add_ecommerce, remove_ecommerce),
    ]
