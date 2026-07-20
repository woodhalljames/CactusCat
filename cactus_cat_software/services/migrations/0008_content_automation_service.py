from django.db import migrations


def add_content_automation(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    try:
        category = ServiceCategory.objects.get(slug="technical-marketing-growth")
    except ServiceCategory.DoesNotExist:
        return

    ServicePackage.objects.update_or_create(
        slug="automated-content-creation-bot",
        defaults={
            "name": "Automated Content Creation & Publishing Bot",
            "category": category,
            "short_description": (
                "A custom AI-powered bot that writes, schedules, and publishes content across your channels automatically. "
                "Built around your brand voice, posted without you touching it."
            ),
            "features": (
                "AI content generation trained on your brand voice and tone\n"
                "Automated publishing to Instagram, LinkedIn, Facebook, X, and more\n"
                "Content calendar built and managed by the system\n"
                "Blog post and newsletter drafts generated on a schedule\n"
                "Hashtag research and SEO optimisation baked in\n"
                "One-click approval flow so you review before anything goes live\n"
                "Performance reporting delivered to your inbox weekly\n"
                "Content repurposing: one idea turned into five formats automatically"
            ),
            "who_its_for": (
                "Business owners who know they should be posting but never have time\n"
                "Service businesses that need consistent visibility without a marketing team\n"
                "Founders who want content output at scale without hiring a copywriter\n"
                "Companies looking to grow organic reach across multiple platforms simultaneously"
            ),
            "description": (
                "Consistent content is the single highest-ROI marketing activity most businesses never do, "
                "because it takes time they don't have. "
                "We build a custom automation system that handles the entire content pipeline for you: "
                "AI generates the copy in your brand voice, the system schedules it across your channels, "
                "and everything goes live automatically. "
                "You can take as much or as little control as you want, from full autopilot to a simple "
                "one-click approval step before anything posts. "
                "We offer this as two separate engagements or as one combined system: "
                "pure automation (connect your existing content to a publishing pipeline) "
                "or full creation plus automation (AI writes it, the bot posts it). "
                "Either way, your brand stays active and visible without you spending hours on it every week."
            ),
            "price": "3200.00",
            "setup_fee": None,
            "monthly_price": "400.00",
            "is_price_starting_from": True,
            "display_order": 3,
            "estimated_delivery_days": 14,
            "is_active": True,
        },
    )


def remove_content_automation(apps, schema_editor):
    ServicePackage = apps.get_model("services", "ServicePackage")
    ServicePackage.objects.filter(slug="automated-content-creation-bot").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0007_ecommerce_service"),
    ]

    operations = [
        migrations.RunPython(add_content_automation, remove_content_automation),
    ]
