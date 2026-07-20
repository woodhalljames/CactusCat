from django.db import migrations


def move_service(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    try:
        category = ServiceCategory.objects.get(slug="custom-software-development")
    except ServiceCategory.DoesNotExist:
        return

    ServicePackage.objects.filter(slug="forward-deployed-engineering").update(
        category=category,
        display_order=3,
    )


def revert_service(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    try:
        category = ServiceCategory.objects.get(slug="automation-ai-systems")
    except ServiceCategory.DoesNotExist:
        return

    ServicePackage.objects.filter(slug="forward-deployed-engineering").update(
        category=category,
        display_order=3,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0011_forward_deployed_engineering_team_automation"),
    ]

    operations = [
        migrations.RunPython(move_service, revert_service),
    ]
