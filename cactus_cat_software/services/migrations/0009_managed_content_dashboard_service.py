from django.db import migrations


def add_service(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    try:
        category = ServiceCategory.objects.get(slug="technical-marketing-growth")
    except ServiceCategory.DoesNotExist:
        return

    ServicePackage.objects.update_or_create(
        slug="managed-content-dashboard",
        defaults={
            "name": "Managed Content Dashboard",
            "category": category,
            "short_description": (
                "A dedicated client portal for managing your automated content pipeline. "
                "Review queued posts, approve or edit before publishing, and track what's gone live, all in one place."
            ),
            "features": (
                "Private client dashboard for full content pipeline visibility\n"
                "Approval queue: review, edit, or approve posts before they go live\n"
                "Full autopilot mode or approval-required mode, your choice\n"
                "Published content log with dates, platforms, and performance notes\n"
                "Direct line to your account manager for content direction changes\n"
                "Weekly summary report delivered automatically\n"
                "Integrates with the automated content creation and publishing bot"
            ),
            "who_its_for": (
                "Clients running the automated content bot who want full visibility and control\n"
                "Business owners managing multiple social channels who need one place to oversee everything\n"
                "Teams that want content running on autopilot but need sign-off before anything posts"
            ),
            "description": (
                "Automation without visibility is a black box, and a black box is hard to trust. "
                "The Managed Content Dashboard gives you a private portal where you can see exactly what your "
                "content bot is doing: what's queued, what's been approved, and what's live across every platform. "
                "You choose how much control you want. "
                "Run it on full autopilot and check in when you feel like it, "
                "or switch to approval mode and spend two minutes a week clicking approve on a handful of posts. "
                "Either way, nothing happens without you having the option to see it. "
                "This is offered as a managed retainer add-on alongside our automated content creation service, "
                "or as a standalone management layer if you're already running your own content pipeline."
            ),
            "price": "0.00",
            "setup_fee": None,
            "monthly_price": None,
            "is_price_starting_from": False,
            "display_order": 4,
            "estimated_delivery_days": None,
            "is_active": True,
        },
    )


def remove_service(apps, schema_editor):
    ServicePackage = apps.get_model("services", "ServicePackage")
    ServicePackage.objects.filter(slug="managed-content-dashboard").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0008_content_automation_service"),
    ]

    operations = [
        migrations.RunPython(add_service, remove_service),
    ]
