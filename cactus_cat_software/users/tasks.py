from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import AccountInvite, User


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@shared_task()
def send_invite_email(invite_id: int, accept_url: str):
    """Send a team invite email to the invited address."""
    try:
        invite = AccountInvite.objects.select_related("inviter").get(pk=invite_id)
    except AccountInvite.DoesNotExist:
        return

    inviter_name = invite.inviter.name or invite.inviter.email
    inviter_company = invite.inviter.company_name or "Cactus Cat Software"

    subject = f"{inviter_name} invited you to their project dashboard"
    message = (
        f"Hi,\n\n"
        f"{inviter_name} ({invite.inviter.email}) at {inviter_company} has invited you to "
        f"join their project dashboard on Cactus Cat Software.\n\n"
        f"As a team member you will be able to view all active projects, milestones, "
        f"deliverables, and updates in real time.\n\n"
        f"Accept your invitation:\n{accept_url}\n\n"
        f"If you don't have an account yet, you'll be prompted to create one first.\n\n"
        f"This invite link is unique to you. Do not share it.\n\n"
        f"-- Cactus Cat Software"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invite.email],
        fail_silently=False,
    )

    return f"Invite sent to {invite.email}"
