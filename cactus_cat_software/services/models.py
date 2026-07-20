from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class ServiceCategory(TimeStampedModel):
    """Main service categories (Custom Software, Automation & AI, Technical Marketing, Infrastructure)"""

    name = models.CharField(_("Category Name"), max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(
        _("Icon Class"),
        max_length=50,
        blank=True,
        help_text="Bootstrap icon class",
    )
    display_order = models.IntegerField(_("Display Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class ServicePackage(TimeStampedModel):
    """Individual service packages within categories"""

    # Basic info
    name = models.CharField(_("Package Name"), max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="packages",
        verbose_name=_("Category"),
    )

    # Descriptions (hierarchy: short -> features -> full)
    short_description = models.CharField(
        _("Short Description"),
        max_length=255,
        help_text="Brief description for catalog cards",
    )
    features = models.TextField(
        _("Features"),
        help_text="One feature per line",
    )
    who_its_for = models.TextField(
        _("Who It's For"),
        blank=True,
        help_text="One ideal client type per line (e.g. 'Small business owners', 'SaaS founders')",
    )
    description = models.TextField(
        _("Full Description"),
        help_text="Detailed description for service detail page",
    )

    # Pricing & media
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    setup_fee = models.DecimalField(
        _("Financing Setup Fee"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Upfront deposit for the financed/subscription option",
    )
    monthly_price = models.DecimalField(
        _("Monthly Financing Price"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monthly rate for the financed option (shown in financing popup)",
    )
    is_price_starting_from = models.BooleanField(
        _("Starting From Price"),
        default=False,
        help_text='Display as "Starting from $X"',
    )
    image = models.ImageField(
        _("Package Image"),
        upload_to="services/",
        blank=True,
    )

    # Display
    is_active = models.BooleanField(_("Active"), default=True)
    display_order = models.IntegerField(_("Display Order"), default=0)
    estimated_delivery_days = models.IntegerField(
        _("Estimated Delivery (Days)"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Service Package")
        verbose_name_plural = _("Service Packages")
        ordering = ["category", "display_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})

    def get_features_list(self):
        return [f.strip() for f in self.features.split("\n") if f.strip()]

    def get_who_its_for_list(self):
        return [w.strip() for w in self.who_its_for.split("\n") if w.strip()]
