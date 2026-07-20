from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_order_pricing_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="budget_range",
            field=models.CharField(
                blank=True,
                help_text="Client's stated budget or range",
                max_length=100,
                verbose_name="Budget Range",
            ),
        ),
    ]
