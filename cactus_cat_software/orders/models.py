import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel):
    """Orders placed by customers (guest or authenticated)."""

    # Unique identifier
    order_number = models.CharField(
        _("Order Number"),
        max_length=32,
        unique=True,
        editable=False,
    )

    # Customer (optional - for guest checkout)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name=_("User"),
    )

    # Contact Information (required for all orders)
    customer_email = models.EmailField(_("Customer Email"))
    customer_name = models.CharField(_("Customer Name"), max_length=200)
    customer_phone = models.CharField(_("Phone Number"), max_length=20, blank=True)

    # Company Information
    company_name = models.CharField(_("Company Name"), max_length=200, blank=True)

    # Timeline
    TIMELINE_CHOICES = [
        ("asap", "As soon as possible"),
        ("1_month", "Within 1 month"),
        ("1_3_months", "1 – 3 months"),
        ("3_6_months", "3 – 6 months"),
        ("flexible", "Flexible / just exploring"),
    ]
    timeline = models.CharField(
        _("Timeline"),
        max_length=20,
        choices=TIMELINE_CHOICES,
        blank=True,
    )

    # Order Details (for legacy single-item orders)
    service_package = models.ForeignKey(
        "services.ServicePackage",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("Service Package"),
        null=True,
        blank=True,
    )
    budget_range = models.CharField(
        _("Budget Range"),
        max_length=100,
        blank=True,
        help_text="Client's stated budget or range",
    )
    custom_requirements = models.TextField(
        _("Custom Requirements"),
        blank=True,
        help_text="Special requests or requirements",
    )

    # Pricing
    PRICING_TYPE_BUYOUT = "buyout"
    PRICING_TYPE_SUBSCRIPTION = "subscription"
    PRICING_TYPE_CHOICES = [
        (PRICING_TYPE_BUYOUT, _("Buyout (Own)")),
        (PRICING_TYPE_SUBSCRIPTION, _("Monthly Subscription")),
    ]
    pricing_type = models.CharField(
        _("Pricing Type"),
        max_length=20,
        choices=PRICING_TYPE_CHOICES,
        default=PRICING_TYPE_BUYOUT,
    )
    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=10,
        decimal_places=2,
    )

    # Internal Notes
    admin_notes = models.TextField(
        _("Admin Notes"),
        blank=True,
        help_text="Internal notes (not visible to customer)",
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["order_number"]),
            models.Index(fields=["customer_email"]),
        ]

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        """Generate unique order number."""
        return f"CC-{uuid.uuid4().hex[:12].upper()}"

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={"order_number": self.order_number})


class OrderItem(TimeStampedModel):
    """Individual items in an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order"),
    )
    service_package = models.ForeignKey(
        "services.ServicePackage",
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("Service Package"),
    )
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price at time of order",
    )

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ["id"]

    def __str__(self):
        return f"{self.quantity}x {self.service_package.name}"

    def get_total_price(self):
        if self.price is None:
            return 0
        return self.price * self.quantity
