from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

TIMELINE_LABELS = {
    "asap": "As soon as possible",
    "1_month": "Within 1 month",
    "1_3_months": "1 – 3 months",
    "3_6_months": "3 – 6 months",
    "flexible": "Flexible / just exploring",
}


@shared_task()
def send_quote_request_email(name, email, service_name, budget_range, goals, timeline):
    timeline_label = TIMELINE_LABELS.get(timeline, timeline)

    message = f"""New quote request for: {service_name}

From:     {name} <{email}>
Budget:   {budget_range}
Timeline: {timeline_label}

Goals / What they're trying to achieve:
{goals}
"""
    send_mail(
        subject=f"Quote Request: {service_name}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin[1] for admin in settings.ADMINS],
    )
    return f"Sent quote request for {service_name} from {email}"
