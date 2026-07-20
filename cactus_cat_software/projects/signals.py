from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender="projects.Project")
def add_team_members_to_new_project(sender, instance, created, **kwargs):
    """When a new project is created, add all accepted team members as collaborators."""
    if not created:
        return

    from cactus_cat_software.users.models import AccountInvite

    accepted = AccountInvite.objects.filter(
        inviter=instance.client,
        accepted=True,
        accepted_by__isnull=False,
    ).select_related("accepted_by")

    for invite in accepted:
        instance.collaborators.add(invite.accepted_by)
