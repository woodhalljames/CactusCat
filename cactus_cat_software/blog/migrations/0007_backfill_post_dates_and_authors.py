import datetime
from django.db import migrations

POST_UPDATES = [
    {
        "slug": "when-cloudflare-goes-down",
        "published_date": datetime.datetime(2023, 10, 15, 9, 0, 0, tzinfo=datetime.timezone.utc),
    },
    {
        "slug": "the-real-cost-of-shopify-and-wix",
        "published_date": datetime.datetime(2024, 2, 12, 9, 0, 0, tzinfo=datetime.timezone.utc),
    },
    {
        "slug": "data-centers-own-your-software",
        "published_date": datetime.datetime(2024, 6, 10, 9, 0, 0, tzinfo=datetime.timezone.utc),
    },
    {
        "slug": "hidden-cost-of-manual-processes",
        "published_date": datetime.datetime(2024, 10, 8, 9, 0, 0, tzinfo=datetime.timezone.utc),
    },
]


def backfill_posts(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    for update in POST_UPDATES:
        BlogPost.objects.filter(slug=update["slug"]).update(
            published_date=update["published_date"],
            author="James",
        )


def reverse_backfill(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_manual_process_cost_post"),
    ]

    operations = [
        migrations.RunPython(backfill_posts, reverse_backfill),
    ]
