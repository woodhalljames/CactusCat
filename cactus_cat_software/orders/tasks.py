from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order


@shared_task()
def send_order_confirmation_email(order_id):
    """Send order confirmation email to customer."""
    try:
        order = Order.objects.select_related("service_package").prefetch_related("items__service_package").get(id=order_id)
    except Order.DoesNotExist:
        return

    if order.items.exists():
        items_text = "\n".join(
            f"- {item.quantity}x {item.service_package.name}"
            for item in order.items.all()
        )
    else:
        name = order.service_package.name if order.service_package else "N/A"
        items_text = f"- 1x {name}"

    message = f"""Hi {order.customer_name},

Thank you for your quote request with Cactus Cat Software.

Order Number: {order.order_number}
Date: {order.created.strftime("%B %d, %Y")}

Services Requested:
{items_text}
"""

    if order.custom_requirements:
        message += f"\nNotes:\n{order.custom_requirements}\n"

    message += "\nWe'll review your request and be in touch within 24 hours. For questions, contact us at hello@cactuscatsoftware.com\n\n-- Cactus Cat Software"

    send_mail(
        subject=f"Quote Request Received – {order.order_number}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.customer_email],
    )

    send_order_notification_to_host.delay(order_id)

    return f"Sent confirmation email for order {order.order_number}"


@shared_task()
def send_order_notification_to_host(order_id):
    """Send order notification to host email."""
    try:
        order = Order.objects.select_related("service_package").prefetch_related("items__service_package").get(id=order_id)
    except Order.DoesNotExist:
        return

    if order.items.exists():
        items_text = "\n".join(
            f"- {item.quantity}x {item.service_package.name}"
            for item in order.items.all()
        )
    else:
        name = order.service_package.name if order.service_package else "N/A"
        items_text = f"- 1x {name}"

    message = f"""New quote request received.

Order Number: {order.order_number}
Date: {order.created.strftime("%B %d, %Y")}

Customer: {order.customer_name}
Email: {order.customer_email}
Phone: {order.customer_phone or "N/A"}
Company: {order.company_name or "N/A"}

Services Requested:
{items_text}
"""

    if order.custom_requirements:
        message += f"\nNotes:\n{order.custom_requirements}\n"

    send_mail(
        subject=f"New Quote Request – {order.order_number}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["cactuscatllc@gmail.com"],
    )

    return f"Sent host notification for order {order.order_number}"
