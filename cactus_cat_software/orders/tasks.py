from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Order
from .utils import generate_order_receipt_pdf


@shared_task()
def send_order_confirmation_email(order_id):
    """Send order confirmation email to customer with PDF receipt."""
    try:
        order = Order.objects.select_related("service_package").prefetch_related("items__service_package").get(id=order_id)
    except Order.DoesNotExist:
        return

    # Generate PDF receipt
    pdf_buffer = generate_order_receipt_pdf(order)

    # Render email templates
    subject = f"Order Confirmation - {order.order_number}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.customer_email

    context = {
        "order": order,
        "site_name": "Cactus Cat Software",
    }

    text_content = render_to_string("orders/emails/order_receipt.txt", context)
    html_content = render_to_string("orders/emails/order_receipt.html", context)

    # Create email with PDF attachment
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    # Attach PDF receipt
    msg.attach(
        f"receipt_{order.order_number}.pdf",
        pdf_buffer.read(),
        "application/pdf"
    )

    msg.send()

    # Send notification to host
    send_order_notification_to_host.delay(order_id)

    return f"Sent confirmation email for order {order.order_number}"


@shared_task()
def send_order_notification_to_host(order_id):
    """Send order notification to host email."""
    try:
        order = Order.objects.select_related("service_package").prefetch_related("items__service_package").get(id=order_id)
    except Order.DoesNotExist:
        return

    # Host email
    host_email = "hello@cactuscatsoftware.com"

    # Render email templates
    subject = f"New Order Received - {order.order_number}"
    from_email = settings.DEFAULT_FROM_EMAIL

    context = {
        "order": order,
        "site_name": "Cactus Cat Software",
    }

    text_content = render_to_string("orders/emails/host_notification.txt", context)
    html_content = render_to_string("orders/emails/host_notification.html", context)

    # Create email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [host_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return f"Sent host notification for order {order.order_number}"
