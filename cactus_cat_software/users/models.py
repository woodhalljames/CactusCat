
import uuid
from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Cactus Cat Software.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    ACCOUNT_TYPE_CHOICES = [
        ("student", _("Student")),
        ("business_applicant", _("Business — Pending Approval")),
        ("business", _("Business")),
    ]

    account_type = CharField(
        _("Account Type"),
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default="student",
    )

    # Business information
    company_name = CharField(_("Company Name"), blank=True, max_length=255)
    phone_number = CharField(_("Phone Number"), blank=True, max_length=20)
    website = CharField(_("Website"), blank=True, max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's dashboard.

        Returns:
            str: URL for user dashboard.

        """
        return reverse("projects:dashboard")


class AccountInvite(TimeStampedModel):
    """Invite a coworker to share access to the account dashboard."""

    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_invites",
    )
    email = models.EmailField(_("Invited Email"))
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    accepted = models.BooleanField(default=False)
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="received_invites",
    )

    class Meta:
        verbose_name = _("Account Invite")
        verbose_name_plural = _("Account Invites")
        unique_together = [("inviter", "email")]
        ordering = ["-created"]

    def __str__(self):
        return f"Invite from {self.inviter.email} to {self.email}"


class NewsletterSubscriber(TimeStampedModel):
    """Newsletter subscribers."""

    email = models.EmailField(_("Email"), unique=True)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Newsletter Subscriber")
        verbose_name_plural = _("Newsletter Subscribers")

    def __str__(self):
        return self.email
