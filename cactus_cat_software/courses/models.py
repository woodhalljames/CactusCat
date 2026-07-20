import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Business(TimeStampedModel):
    """An organisation that hosts courses on the platform."""

    name = models.CharField(_("Business Name"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True)
    url = models.URLField(
        _("Website"),
        blank=True,
        help_text="Public website for this business",
    )
    description = models.TextField(_("Description"), blank=True)
    logo = models.ImageField(
        _("Logo"),
        upload_to="logos/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(_("Active"), default=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="owned_businesses",
        verbose_name=_("Owner"),
    )

    class Meta:
        verbose_name = _("Business")
        verbose_name_plural = _("Businesses")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, n = base, 1
            while Business.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses:business_profile", kwargs={"slug": self.slug})


class BusinessLocation(TimeStampedModel):
    """A physical or named location/classroom belonging to a business."""

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name=_("Business"),
    )
    name = models.CharField(
        _("Location Name"),
        max_length=200,
        help_text="e.g. Downtown Branch, Chicago Office, Classroom A",
    )
    address = models.CharField(_("Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State / Region"), max_length=100, blank=True)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Business Location")
        verbose_name_plural = _("Business Locations")
        ordering = ["business", "name"]

    def __str__(self):
        parts = [self.name]
        if self.city:
            parts.append(self.city)
        return f"{self.business.name} — {', '.join(parts)}"


class BusinessApplication(TimeStampedModel):
    """A request from a user to become a business account on the platform."""

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, _("Pending Review")),
        (STATUS_APPROVED, _("Approved")),
        (STATUS_REJECTED, _("Rejected")),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_application",
        verbose_name=_("Applicant"),
    )
    business_name = models.CharField(_("Business Name"), max_length=200)
    business_url = models.URLField(_("Business Website"), blank=True)
    description = models.TextField(
        _("About Your Business"),
        blank=True,
        help_text="What does your business do? What courses do you plan to offer?",
    )
    google_profile_url = models.URLField(
        _("Google Business Profile URL"),
        blank=True,
        help_text="Link to your Google Business Profile for verification",
    )
    is_google_verified = models.BooleanField(
        _("Google Verified"),
        default=False,
        help_text="Set automatically when applicant has a linked Google account",
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    admin_notes = models.TextField(_("Admin Notes"), blank=True)
    linked_business = models.OneToOneField(
        Business,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="application",
        verbose_name=_("Linked Business"),
    )

    class Meta:
        verbose_name = _("Business Application")
        verbose_name_plural = _("Business Applications")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.business_name} ({self.user.email}) — {self.get_status_display()}"


class Teacher(TimeStampedModel):
    """An instructor who belongs to a business and can be assigned to courses."""

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="teachers",
        verbose_name=_("Business"),
    )
    location = models.ForeignKey(
        BusinessLocation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="teachers",
        verbose_name=_("Location"),
    )
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True)
    name = models.CharField(_("Full Name"), max_length=200)
    title = models.CharField(
        _("Title / Role"),
        max_length=200,
        blank=True,
        help_text="e.g. Lead Instructor, Senior Developer",
    )
    email = models.EmailField(_("Email"), blank=True)
    bio = models.TextField(_("Bio"), blank=True)
    url = models.URLField(
        _("Profile URL"),
        blank=True,
        help_text="Personal site, LinkedIn, etc.",
    )
    photo = models.ImageField(
        _("Photo"),
        upload_to="teachers/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        ordering = ["business", "name"]

    def __str__(self):
        return f"{self.name} — {self.business.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.business.name}-{self.name}")
            slug, n = base, 1
            while Teacher.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses:teacher_profile", kwargs={"slug": self.slug})


class Course(TimeStampedModel):
    """A course offered by a business and taught by one or more teachers."""

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name=_("Business"),
    )
    location = models.ForeignKey(
        BusinessLocation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="courses",
        verbose_name=_("Location / Classroom"),
        help_text="Optional: tie this course to a specific location or classroom",
    )
    teachers = models.ManyToManyField(
        Teacher,
        related_name="courses",
        verbose_name=_("Teachers"),
        blank=True,
        help_text="At least one teacher is required to open registration",
    )
    title = models.CharField(_("Course Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    skills = models.TextField(
        _("Skills Taught"),
        blank=True,
        help_text="One skill per line (e.g. Python, Django, REST APIs)",
    )
    is_open = models.BooleanField(
        _("Open for Registration"),
        default=False,
        help_text="Requires at least one teacher assigned before enabling",
    )
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ["business", "title"]

    def __str__(self):
        return f"{self.title} — {self.business.name}"

    def clean(self):
        if self.is_open and self.pk:
            if not self.teachers.exists():
                raise ValidationError(
                    {"is_open": "At least one teacher must be assigned before opening registration."}
                )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.business.name}-{self.title}")
            slug, n = base, 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_skills_list(self):
        return [s.strip() for s in self.skills.splitlines() if s.strip()]


class Enrollment(TimeStampedModel):
    """A student's enrollment in a course."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name=_("Student"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name=_("Course"),
    )
    is_completed = models.BooleanField(_("Completed"), default=False)
    completed_date = models.DateField(_("Completion Date"), null=True, blank=True)

    certificate_id = models.UUIDField(
        _("Certificate ID"),
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")
        unique_together = [("student", "course")]
        ordering = ["-created"]

    def __str__(self):
        status = "✓" if self.is_completed else "…"
        return f"{self.student.email} → {self.course.title} [{status}]"

    def get_certificate_url(self):
        return reverse("courses:certificate", kwargs={"cert_id": self.certificate_id})


class BusinessComment(TimeStampedModel):
    """A public comment left on a business profile."""

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Business"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_comments",
        verbose_name=_("Author"),
    )
    body = models.TextField(_("Comment"), max_length=1000)
    is_visible = models.BooleanField(
        _("Visible"),
        default=True,
        help_text="Uncheck to hide spam or abusive comments",
    )

    class Meta:
        verbose_name = _("Business Comment")
        verbose_name_plural = _("Business Comments")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.author.email} on {self.business.name}"


class StudentProfile(TimeStampedModel):
    """Controls a student's public share page."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
        verbose_name=_("User"),
    )
    display_name = models.CharField(
        _("Display Name / Alias"),
        max_length=100,
        blank=True,
        help_text="Public alias shown instead of real name. Leave blank to use username.",
    )
    bio = models.TextField(
        _("Bio"),
        max_length=500,
        blank=True,
        help_text="Short public bio (max 500 characters)",
    )
    profile_photo = models.ImageField(
        _("Profile Photo"),
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    share_token = models.UUIDField(
        _("Share Token"),
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    is_public = models.BooleanField(
        _("Public Profile"),
        default=False,
        help_text="When off: share link shows username + join date + photo only. When on: completed courses are visible.",
    )

    class Meta:
        verbose_name = _("Student Profile")
        verbose_name_plural = _("Student Profiles")

    def __str__(self):
        return f"Profile: {self.user.email}"

    def get_public_url(self):
        return reverse("courses:public_profile", kwargs={"token": self.share_token})

    def get_display_name(self):
        return self.display_name or self.user.name or self.user.email.split("@")[0]

    def completed_enrollments(self):
        return (
            self.user.enrollments
            .filter(is_completed=True)
            .select_related("course", "course__business")
            .prefetch_related("course__teachers")
        )
