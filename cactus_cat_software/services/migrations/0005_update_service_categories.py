from django.db import migrations

NEW_CATEGORIES = [
    {
        "name": "Custom Software Development",
        "slug": "custom-software-development",
        "description": "Web apps, SaaS platforms, customer portals, internal tools, and APIs. All custom-built around how your business operates. You own everything from day one.",
        "icon": "bi-code-square",
        "display_order": 1,
    },
    {
        "name": "Automation & AI Systems",
        "slug": "automation-ai-systems",
        "description": "Workflow automation, AI integrations, CRM automation, data sync, and custom scripts that eliminate manual work permanently. ROI visible by day 30.",
        "icon": "bi-gear-wide-connected",
        "display_order": 2,
    },
    {
        "name": "Technical Marketing & Growth",
        "slug": "technical-marketing-growth",
        "description": "The technical foundation behind scalable marketing: SEO, analytics, landing pages, funnel systems, and lead generation infrastructure.",
        "icon": "bi-graph-up-arrow",
        "display_order": 3,
    },
    {
        "name": "Infrastructure & Support",
        "slug": "infrastructure-support",
        "description": "Hosting, deployment, maintenance, security updates, performance monitoring, and DevOps. Ongoing support that keeps your systems running smoothly.",
        "icon": "bi-server",
        "display_order": 4,
    },
]

KEEP_SLUGS = {c["slug"] for c in NEW_CATEGORIES}


def update_categories(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")

    # Deactivate any category not in the new set
    ServiceCategory.objects.exclude(slug__in=KEEP_SLUGS).update(is_active=False)

    # Upsert each new category
    for cat in NEW_CATEGORIES:
        ServiceCategory.objects.update_or_create(
            slug=cat["slug"],
            defaults={
                "name": cat["name"],
                "description": cat["description"],
                "icon": cat["icon"],
                "display_order": cat["display_order"],
                "is_active": True,
            },
        )


def reverse_categories(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServiceCategory.objects.filter(slug__in=KEEP_SLUGS).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0004_servicepackage_who_its_for"),
    ]

    operations = [
        migrations.RunPython(update_categories, reverse_categories),
    ]
