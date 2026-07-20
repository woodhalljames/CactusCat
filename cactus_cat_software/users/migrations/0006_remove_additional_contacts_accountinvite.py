import uuid
import django.db.models.deletion
import model_utils.fields
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_user_account_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="additional_contacts",
        ),
        migrations.CreateModel(
            name="AccountInvite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name="created")),
                ("modified", model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name="modified")),
                ("email", models.EmailField(max_length=254, verbose_name="Invited Email")),
                ("token", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("accepted", models.BooleanField(default=False)),
                ("accepted_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="received_invites", to=settings.AUTH_USER_MODEL)),
                ("inviter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sent_invites", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Account Invite",
                "verbose_name_plural": "Account Invites",
                "ordering": ["-created"],
                "unique_together": {("inviter", "email")},
            },
        ),
    ]
