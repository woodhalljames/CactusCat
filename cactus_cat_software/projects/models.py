from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Project(TimeStampedModel):
    """Client projects linked to orders."""

    STATUS_CHOICES = [
        ("not_started", _("Not Started")),
        ("planning", _("Planning")),
        ("design", _("Design")),
        ("development", _("Development")),
        ("review", _("Review")),
        ("completed", _("Completed")),
    ]

    # Link to order
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="project",
        verbose_name=_("Order"),
    )

    # Client access
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name=_("Client"),
        help_text="User who can view this project",
    )

    # Project Info
    project_name = models.CharField(_("Project Name"), max_length=200)
    slug = models.SlugField(
        _("Slug"),
        max_length=220,
        unique=True,
        blank=True,
        help_text="Auto-generated from project name",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started",
    )
    progress_percentage = models.IntegerField(_("Progress %"), default=0)

    # Dates
    estimated_completion = models.DateField(
        _("Estimated Completion"),
        null=True,
        blank=True,
    )
    actual_completion = models.DateField(
        _("Actual Completion"),
        null=True,
        blank=True,
    )

    # Notes
    status_notes = models.TextField(
        _("Status Notes"),
        blank=True,
        help_text="Current status description for client",
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.project_name} - {self.client.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.project_name)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"pk": self.pk})


class ProjectUpdate(TimeStampedModel):
    """Design mockups/images for client review."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="updates",
        verbose_name=_("Project"),
    )

    title = models.CharField(_("Update Title"), max_length=200)
    description = models.TextField(_("Description"))
    image = models.ImageField(_("Update Image"), upload_to="project_updates/")

    # Client feedback
    requires_approval = models.BooleanField(_("Requires Approval"), default=False)
    approved = models.BooleanField(_("Approved"), default=False)
    client_feedback = models.TextField(_("Client Feedback"), blank=True)

    class Meta:
        verbose_name = _("Project Update")
        verbose_name_plural = _("Project Updates")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.project.project_name} - {self.title}"


class ProjectInvoice(TimeStampedModel):
    """Billing records for client view."""

    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("sent", _("Sent")),
        ("paid", _("Paid")),
        ("overdue", _("Overdue")),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="invoices",
        verbose_name=_("Project"),
    )

    invoice_number = models.CharField(
        _("Invoice Number"),
        max_length=50,
        unique=True,
    )
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    due_date = models.DateField(_("Due Date"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    # Payment tracking
    paid_date = models.DateField(_("Paid Date"), null=True, blank=True)
    payment_method = models.CharField(
        _("Payment Method"),
        max_length=100,
        blank=True,
    )

    # Files
    invoice_file = models.FileField(
        _("Invoice PDF"),
        upload_to="invoices/",
        blank=True,
    )

    class Meta:
        verbose_name = _("Project Invoice")
        verbose_name_plural = _("Project Invoices")
        ordering = ["-created"]

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.project.project_name}"


class ProjectItem(TimeStampedModel):
    """Individual deliverables/tasks within a project."""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("in_progress", _("In Progress")),
        ("review", _("In Review")),
        ("completed", _("Completed")),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Project"),
    )

    # Item details
    name = models.CharField(_("Item Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    progress_percentage = models.IntegerField(_("Progress %"), default=0)

    # Ordering
    display_order = models.IntegerField(_("Display Order"), default=0)

    # Dates
    due_date = models.DateField(_("Due Date"), null=True, blank=True)
    completed_date = models.DateField(_("Completed Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Project Item")
        verbose_name_plural = _("Project Items")
        ordering = ["display_order", "created"]

    def __str__(self):
        return f"{self.project.project_name} - {self.name}"


class ProjectNote(TimeStampedModel):
    """Notes and comments for project communication."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name=_("Project"),
    )

    # Optional link to specific item
    item = models.ForeignKey(
        ProjectItem,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name=_("Project Item"),
        null=True,
        blank=True,
        help_text="Link note to specific item (optional)",
    )

    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_notes",
        verbose_name=_("Author"),
    )

    # Content
    content = models.TextField(_("Content"))

    # Threading support
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("Parent Note"),
        null=True,
        blank=True,
        help_text="Reply to another note",
    )

    # Attachments
    attachment = models.FileField(
        _("Attachment"),
        upload_to="project_notes/",
        blank=True,
        help_text="Optional file attachment",
    )

    # Admin features
    is_internal = models.BooleanField(
        _("Internal Note"),
        default=False,
        help_text="Only visible to staff",
    )

    class Meta:
        verbose_name = _("Project Note")
        verbose_name_plural = _("Project Notes")
        ordering = ["created"]

    def __str__(self):
        return f"{self.project.project_name} - Note by {self.author.name or self.author.email}"


class ProjectMilestone(TimeStampedModel):
    """Major project milestones for tracking progress."""

    STATUS_CHOICES = [
        ("not_started", _("Not Started")),
        ("in_progress", _("In Progress")),
        ("completed", _("Completed")),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones",
        verbose_name=_("Project"),
    )

    # Milestone details
    name = models.CharField(_("Milestone Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started",
    )

    # Ordering
    display_order = models.IntegerField(_("Display Order"), default=0)

    # Dates
    target_date = models.DateField(_("Target Date"), null=True, blank=True)
    completion_date = models.DateField(_("Completion Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Project Milestone")
        verbose_name_plural = _("Project Milestones")
        ordering = ["display_order", "target_date"]

    def __str__(self):
        return f"{self.project.project_name} - {self.name}"


class ProjectApproval(TimeStampedModel):
    """Client approvals for deliverables, designs, and documents."""

    STATUS_CHOICES = [
        ("pending", _("Pending Review")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
        ("revised", _("Needs Revision")),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="approvals",
        verbose_name=_("Project"),
    )

    # Approval details
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # Files - supports both images and documents
    document = models.FileField(
        _("Document/Image"),
        upload_to="project_approvals/",
        blank=True,
        help_text="Upload document, image, or design file",
    )

    # Client response
    client_decision_date = models.DateTimeField(
        _("Decision Date"),
        null=True,
        blank=True,
    )
    client_notes = models.TextField(
        _("Client Notes"),
        blank=True,
        help_text="Client feedback or rejection reason",
    )

    # Tracking
    requires_response = models.BooleanField(
        _("Requires Client Response"),
        default=True,
        help_text="Whether client needs to approve/reject",
    )

    class Meta:
        verbose_name = _("Project Approval")
        verbose_name_plural = _("Project Approvals")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.project.project_name} - {self.title} ({self.get_status_display()})"

    def is_pending(self):
        return self.status == "pending"

    def is_approved(self):
        return self.status == "approved"

    def is_rejected(self):
        return self.status == "rejected"
