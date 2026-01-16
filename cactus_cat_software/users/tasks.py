from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import User


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@shared_task()
def send_contact_form_email(name, email, subject, message):
    """Send contact form email to admin."""
    full_message = f"From: {name} <{email}>\n\n{message}"

    send_mail(
        subject=f"Contact Form: {subject}",
        message=full_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin[1] for admin in settings.ADMINS],
    )

    return f"Sent contact form email from {email}"
