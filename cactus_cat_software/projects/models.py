import secrets
import uuid

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
        help_text="Primary client user for this project",
    )

    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collaborated_projects",
        verbose_name=_("Additional Team Members"),
        blank=True,
        help_text="Other users who can view this project dashboard (e.g. client's team members)",
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

    # Preview / Beta Access
    preview_url = models.URLField(
        _("Preview URL"),
        blank=True,
        help_text="Link to the current beta build on the VPS (e.g. http://123.45.67.89:8080)",
    )
    beta_username = models.CharField(
        _("Beta Username"),
        max_length=200,
        blank=True,
        help_text="Test account username for the beta site (visible to client)",
    )
    beta_password = models.CharField(
        _("Beta Password"),
        max_length=200,
        blank=True,
        help_text="Test account password for the beta site (visible to client)",
    )

    # Account Manager
    account_manager_name = models.CharField(
        _("Account Manager Name"),
        max_length=200,
        blank=True,
    )
    account_manager_title = models.CharField(
        _("Account Manager Title"),
        max_length=200,
        blank=True,
        help_text="e.g. Project Lead, Creative Director",
    )
    account_manager_email = models.EmailField(
        _("Account Manager Email"),
        blank=True,
    )
    account_manager_phone = models.CharField(
        _("Account Manager Phone"),
        max_length=50,
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

    def get_service_slug(self):
        if self.order.service_package:
            return self.order.service_package.slug
        first_item = self.order.items.first()
        return first_item.service_package.slug if first_item else "project"

    def get_absolute_url(self):
        return reverse(
            "projects:detail",
            kwargs={
                "service_slug": self.get_service_slug(),
                "order_number": self.order.order_number,
            },
        )


class ProjectPhase(TimeStampedModel):
    """A custom project phase created by the admin (e.g. Discovery, Architecture, QA)."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="phases",
        verbose_name=_("Project"),
    )

    name = models.CharField(
        _("Phase Name"),
        max_length=200,
        help_text="e.g. Discovery, Scope Definition, Architecture, Development",
    )
    description = models.TextField(
        _("Client Notes"),
        blank=True,
        help_text="Updates or notes visible to the client for this phase",
    )
    progress_percentage = models.IntegerField(
        _("Progress %"),
        default=0,
        help_text="0–100. Admin sets this; client sees the progress bar.",
    )
    display_order = models.IntegerField(_("Display Order"), default=0)

    class Meta:
        verbose_name = _("Project Phase")
        verbose_name_plural = _("Project Phases")
        ordering = ["display_order", "created"]

    def __str__(self):
        return f"{self.project.project_name} — {self.name}"


class ProjectUpdate(TimeStampedModel):
    """Design mockups/images for client review."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="updates",
        verbose_name=_("Project"),
    )

    phase = models.ForeignKey(
        ProjectPhase,
        on_delete=models.SET_NULL,
        related_name="updates",
        verbose_name=_("Phase"),
        null=True,
        blank=True,
        help_text="Link to a specific project phase (optional)",
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

    # Payment link (e.g. PayPal, Stripe, Square, etc.)
    payment_url = models.URLField(
        _("Payment Link"),
        blank=True,
        help_text="Optional external payment link (PayPal, Stripe, Square, etc.)",
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

    phase = models.ForeignKey(
        "ProjectPhase",
        on_delete=models.SET_NULL,
        related_name="items",
        verbose_name=_("Phase"),
        null=True,
        blank=True,
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


class ProjectQuestion(TimeStampedModel):
    """A question the admin posts for the client to answer within a phase."""

    TYPE_CHOICES = [
        ("text", _("Free Text")),
        ("confirm", _("Confirm / Acknowledge")),
        ("choice", _("Select from Options")),
    ]

    STATUS_CHOICES = [
        ("pending", _("Awaiting Response")),
        ("answered", _("Answered")),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("Project"),
    )

    phase = models.ForeignKey(
        ProjectPhase,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("Phase"),
        null=True,
        blank=True,
        help_text="Which phase this question belongs to",
    )

    question = models.TextField(_("Question"), help_text="The question or instruction shown to the client")
    question_type = models.CharField(
        _("Question Type"),
        max_length=10,
        choices=TYPE_CHOICES,
        default="text",
        help_text="Free Text = client writes an answer. Confirm = client ticks a checkbox. Choice = client picks from a list.",
    )
    choices = models.TextField(
        _("Options"),
        blank=True,
        help_text="For 'Select from Options' type only — one option per line (e.g. brand slogans, language tones).",
    )

    # Optional media/doc the admin attaches to provide context
    attachment = models.FileField(
        _("Attachment"),
        upload_to="project_questions/",
        blank=True,
        help_text="Optional image, PDF, or document the client should review before answering",
    )

    display_order = models.IntegerField(_("Display Order"), default=0)

    # Client response
    answer = models.TextField(_("Client Answer"), blank=True)
    answered_at = models.DateTimeField(_("Answered At"), null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        verbose_name = _("Project Question")
        verbose_name_plural = _("Project Questions")
        ordering = ["display_order", "created"]

    def __str__(self):
        return f"{self.project.project_name} — Q: {self.question[:60]}"

    def get_choices_list(self):
        """Return choices as a list of stripped strings."""
        return [c.strip() for c in self.choices.splitlines() if c.strip()]


class ProjectNote(TimeStampedModel):
    """Notes and comments for project communication."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name=_("Project"),
    )

    # Optional link to phase or specific item
    phase = models.ForeignKey(
        "ProjectPhase",
        on_delete=models.SET_NULL,
        related_name="notes",
        verbose_name=_("Phase"),
        null=True,
        blank=True,
    )

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

    phase = models.ForeignKey(
        "ProjectPhase",
        on_delete=models.SET_NULL,
        related_name="milestones",
        verbose_name=_("Phase"),
        null=True,
        blank=True,
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

    phase = models.ForeignKey(
        "ProjectPhase",
        on_delete=models.SET_NULL,
        related_name="approvals",
        verbose_name=_("Phase"),
        null=True,
        blank=True,
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


class ProjectDeployment(TimeStampedModel):
    """Docker deployment configuration for client project previews."""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("cloning", _("Cloning Repository")),
        ("building", _("Building Image")),
        ("starting", _("Starting Container")),
        ("running", _("Running")),
        ("stopped", _("Stopped")),
        ("failed", _("Failed")),
    ]

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="deployment",
        verbose_name=_("Project"),
    )

    # GitHub configuration
    github_repo_url = models.URLField(
        _("GitHub Repository URL"),
        help_text="Full URL to the GitHub repository (e.g., https://github.com/user/repo)",
    )
    github_branch = models.CharField(
        _("Branch"),
        max_length=100,
        default="main",
        help_text="Branch to deploy (default: main)",
    )
    webhook_secret = models.CharField(
        _("Webhook Secret"),
        max_length=64,
        blank=True,
        help_text="Secret for validating GitHub webhook requests",
    )

    # Container configuration
    container_id = models.CharField(
        _("Container ID"),
        max_length=64,
        blank=True,
        help_text="Docker container ID when running",
    )
    image_name = models.CharField(
        _("Image Name"),
        max_length=200,
        blank=True,
        help_text="Docker image name for this deployment",
    )
    internal_port = models.IntegerField(
        _("Internal Port"),
        default=8000,
        help_text="Port the application listens on inside the container",
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    last_deployed_at = models.DateTimeField(
        _("Last Deployed"),
        null=True,
        blank=True,
    )
    build_log = models.TextField(
        _("Build Log"),
        blank=True,
        help_text="Output from the last build/deploy attempt",
    )

    # Public access
    preview_token = models.UUIDField(
        _("Preview Token"),
        default=uuid.uuid4,
        unique=True,
        help_text="Token for public preview access",
    )

    # Resource limits
    memory_limit = models.CharField(
        _("Memory Limit"),
        max_length=20,
        default="256m",
        help_text="Container memory limit (e.g., 256m, 512m)",
    )
    cpu_limit = models.FloatField(
        _("CPU Limit"),
        default=0.5,
        help_text="CPU limit (0.5 = half a core)",
    )

    class Meta:
        verbose_name = _("Project Deployment")
        verbose_name_plural = _("Project Deployments")

    def __str__(self):
        return f"Deployment: {self.project.project_name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.webhook_secret:
            self.webhook_secret = secrets.token_hex(32)
        if not self.image_name:
            self.image_name = f"client-{self.project.slug}:latest"
        super().save(*args, **kwargs)

    def get_preview_url(self):
        """Get the path-based preview URL."""
        return f"/{self.project.slug}-preview/"

    def get_preview_link(self):
        """Get the full preview URL with token for clients."""
        return reverse("projects:preview", kwargs={"token": self.preview_token})

    def get_webhook_url(self):
        """Get the webhook URL for GitHub."""
        return reverse("projects:github_webhook", kwargs={"project_id": self.project.pk})

    def is_running(self):
        return self.status == "running"

    def is_deploying(self):
        return self.status in ("cloning", "building", "starting")

    def can_deploy(self):
        return self.status in ("pending", "stopped", "failed")

    def can_stop(self):
        return self.status == "running"
