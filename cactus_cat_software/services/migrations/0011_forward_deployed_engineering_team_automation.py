from django.db import migrations


def add_services(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    try:
        custom_software_category = ServiceCategory.objects.get(slug="custom-software-development")
        automation_category = ServiceCategory.objects.get(slug="automation-ai-systems")
    except ServiceCategory.DoesNotExist:
        return

    ServicePackage.objects.update_or_create(
        slug="forward-deployed-engineering",
        defaults={
            "name": "Forward Deployed Engineering",
            "category": custom_software_category,
            "short_description": (
                "An embedded engineer who works directly inside your team, on-site or async, "
                "shipping the custom software and integrations your operation actually needs, on your timeline."
            ),
            "features": (
                "Dedicated engineer embedded in your team's day-to-day workflow\n"
                "Direct access to your stakeholders, no account manager layer\n"
                "Rapid prototyping and iteration against real operational feedback\n"
                "Integrates with your existing stack, tools, and data sources\n"
                "Weekly shipped increments over a fixed engagement window\n"
                "Full source code and documentation delivered as you go"
            ),
            "who_its_for": (
                "Operations teams with a backlog of custom tooling but no engineer to build it\n"
                "Founders who need a technical partner embedded through a critical build phase\n"
                "Companies deploying software into a complex, non-standard operational environment\n"
                "Teams that need someone in the room translating business needs into shipped code"
            ),
            "description": (
                "Some problems can't be scoped from the outside. They need someone embedded in the "
                "day-to-day of your team, watching how work actually happens, and shipping software "
                "that fits the operation instead of forcing the operation to fit the software. "
                "That's forward deployed engineering: a dedicated engineer working alongside your team, "
                "on-site or async, iterating directly against real feedback instead of a static spec. "
                "You get working software every week, built by someone who understands your operation "
                "because they're inside it, not a deliverable handed over after months of guesswork."
            ),
            "price": "9500.00",
            "setup_fee": None,
            "monthly_price": "8000.00",
            "is_price_starting_from": True,
            "display_order": 3,
            "estimated_delivery_days": None,
            "is_active": True,
        },
    )

    ServicePackage.objects.update_or_create(
        slug="team-automation",
        defaults={
            "name": "Team Automation",
            "category": automation_category,
            "short_description": (
                "A full audit and automation build-out across how your team actually works: approvals, "
                "handoffs, notifications, and cross-tool busywork, replaced with systems that run themselves."
            ),
            "features": (
                "Full workflow audit across your team's tools and processes\n"
                "Automated task routing, approvals, and handoffs between team members\n"
                "Cross-tool orchestration (Slack, email, CRM, project management, and more)\n"
                "Notification and escalation systems so nothing sits waiting on a person\n"
                "Manager-facing dashboard showing what's automated and what still needs a human\n"
                "Full documentation so your team can maintain and extend it"
            ),
            "who_its_for": (
                "Teams where work stalls waiting on someone to notice, approve, or forward it\n"
                "Managers spending hours a week chasing status updates across tools\n"
                "Companies that have automated individual tasks but never the team as a system\n"
                "Growing teams that don't want to hire just to move information around"
            ),
            "description": (
                "Most automation work fixes one task at a time. Team Automation fixes the team. "
                "We audit how work actually moves between your people, across every tool involved, "
                "and replace the manual handoffs, approvals, and status-chasing with systems that run "
                "on their own: routing, notifying, escalating, and reporting without anyone lifting a finger. "
                "The result isn't a script that saves one person an hour, it's an operation that runs "
                "the same way whether you have five people or fifty."
            ),
            "price": "6500.00",
            "setup_fee": None,
            "monthly_price": "500.00",
            "is_price_starting_from": True,
            "display_order": 4,
            "estimated_delivery_days": 28,
            "is_active": True,
        },
    )


def remove_services(apps, schema_editor):
    ServicePackage = apps.get_model("services", "ServicePackage")
    ServicePackage.objects.filter(
        slug__in=["forward-deployed-engineering", "team-automation"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0010_infrastructure_cybersecurity"),
    ]

    operations = [
        migrations.RunPython(add_services, remove_services),
    ]
