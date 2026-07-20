from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_projectdeployment"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="preview_url",
            field=models.URLField(
                blank=True,
                help_text="Link to the current beta build on the VPS (e.g. http://123.45.67.89:8080)",
                verbose_name="Preview URL",
            ),
        ),
    ]
