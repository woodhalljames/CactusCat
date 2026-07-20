from django import forms
from django.contrib import admin
from django.db import models as db_models

from .models import (
    Project,
    ProjectApproval,
    ProjectInvoice,
    ProjectNote,
    ProjectPhase,
    ProjectQuestion,
    ProjectUpdate,
)


class ProjectAdminForm(forms.ModelForm):
    status_notes = forms.CharField(
        label="Status Notes",
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 6,
            "style": "width:100%; background:#fff; color:#111; font-size:14px; border:1px solid #ccc; border-radius:4px; padding:8px;",
        }),
    )

    class Meta:
        model = Project
        fields = "__all__"


class ProjectPhaseMixin:
    """Filter the phase dropdown to only show phases for the current project."""

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "phase":
            project_id = request.resolver_match.kwargs.get("object_id")
            if project_id:
                kwargs["queryset"] = ProjectPhase.objects.filter(project_id=project_id)
            else:
                kwargs["queryset"] = ProjectPhase.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProjectPhaseInline(admin.TabularInline):
    model = ProjectPhase
    extra = 1
    fields = ["name", "progress_percentage", "description", "display_order"]
    ordering = ["display_order"]
    verbose_name = "Phase"
    verbose_name_plural = "Phases (e.g. Discovery, Architecture, Development, QA, Launch)"


class ProjectQuestionInline(ProjectPhaseMixin, admin.StackedInline):
    model = ProjectQuestion
    extra = 1
    fields = ["phase", "question", "question_type", "choices", "attachment", "display_order", "status", "answer", "answered_at"]
    readonly_fields = ["status", "answer", "answered_at"]
    verbose_name = "Client Question"
    verbose_name_plural = "Client Questions"



class ProjectUpdateInline(ProjectPhaseMixin, admin.TabularInline):
    model = ProjectUpdate
    extra = 0
    fields = ["title", "phase", "image", "requires_approval", "approved", "created"]
    readonly_fields = ["created"]


class ProjectInvoiceInline(admin.TabularInline):
    model = ProjectInvoice
    extra = 0
    fields = ["invoice_number", "amount", "due_date", "status", "paid_date", "payment_url", "invoice_file"]



class ProjectNoteInline(ProjectPhaseMixin, admin.StackedInline):
    model = ProjectNote
    extra = 0
    fields = ["author", "phase", "content", "attachment", "is_internal", "parent"]
    readonly_fields = ["created"]


class ProjectApprovalInline(ProjectPhaseMixin, admin.StackedInline):
    model = ProjectApproval
    extra = 0
    fields = ["title", "phase", "description", "document", "requires_response", "status", "client_notes", "client_decision_date"]
    readonly_fields = ["status", "client_notes", "client_decision_date"]
    verbose_name = "Client Review"
    verbose_name_plural = "Client Reviews"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = [
        "project_name",
        "slug",
        "client",
        "status",
        "estimated_completion",
    ]
    list_filter = ["status", "created"]
    search_fields = ["project_name", "slug", "client__email", "order__order_number"]
    readonly_fields = ["slug"]
    filter_horizontal = ["collaborators"]
    inlines = [
        ProjectPhaseInline,
        ProjectQuestionInline,
        ProjectApprovalInline,
        ProjectUpdateInline,
        ProjectInvoiceInline,
        ProjectNoteInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("order", "client", "collaborators", "project_name", "slug"),
            },
        ),
        (
            "Status Notes",
            {
                "fields": ("status_notes",),
            },
        ),
        (
            "Account Manager",
            {
                "fields": ("account_manager_name", "account_manager_title", "account_manager_email", "account_manager_phone"),
            },
        ),
        (
            "Beta / Preview Access",
            {
                "fields": ("preview_url", "beta_username", "beta_password"),
                "description": "Share the staging URL and test login with the client.",
            },
        ),
        (
            "Dates",
            {
                "fields": ("estimated_completion", "actual_completion"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "requires_approval", "approved", "created"]
    list_filter = ["requires_approval", "approved", "created"]
    search_fields = ["title", "project__project_name"]


@admin.register(ProjectInvoice)
class ProjectInvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "project", "amount", "due_date", "status", "has_file"]
    list_filter = ["status", "due_date", "paid_date"]
    search_fields = ["invoice_number", "project__project_name"]
    readonly_fields = ["created", "modified"]

    fieldsets = (
        (
            "Invoice Details",
            {
                "fields": ("project", "invoice_number", "amount", "due_date"),
            },
        ),
        (
            "Status",
            {
                "fields": ("status", "paid_date", "payment_method"),
            },
        ),
        (
            "Document",
            {
                "fields": ("invoice_file",),
                "description": "Upload invoice PDF or document here",
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created", "modified"),
            },
        ),
    )

    def has_file(self, obj):
        return bool(obj.invoice_file)

    has_file.boolean = True
    has_file.short_description = "Has Document"



@admin.register(ProjectNote)
class ProjectNoteAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "author",
        "content_preview",
        "item",
        "is_internal",
        "created",
    ]
    list_filter = ["is_internal", "created", "author"]
    search_fields = ["content", "project__project_name", "author__email"]
    readonly_fields = ["created", "modified"]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Content"



@admin.register(ProjectPhase)
class ProjectPhaseAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "progress_percentage", "display_order"]
    list_filter = ["project"]
    search_fields = ["name", "project__project_name"]
    list_editable = ["progress_percentage", "display_order"]


@admin.register(ProjectQuestion)
class ProjectQuestionAdmin(admin.ModelAdmin):
    list_display = ["question_preview", "project", "phase", "question_type", "status", "created"]
    list_filter = ["status", "question_type", "created"]
    search_fields = ["question", "project__project_name", "answer"]
    readonly_fields = ["status", "answered_at", "created", "modified"]

    def question_preview(self, obj):
        return obj.question[:60] + "..." if len(obj.question) > 60 else obj.question

    question_preview.short_description = "Question"


@admin.register(ProjectApproval)
class ProjectApprovalAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "project",
        "status",
        "requires_response",
        "client_decision_date",
        "created",
    ]
    list_filter = ["status", "requires_response", "created", "client_decision_date"]
    search_fields = ["title", "description", "project__project_name", "client_notes"]
    readonly_fields = ["created", "modified", "client_decision_date"]

    fieldsets = (
        (
            "Approval Details",
            {
                "fields": ("project", "phase", "title", "description", "document"),
            },
        ),
        (
            "Status",
            {
                "fields": ("status", "requires_response"),
            },
        ),
        (
            "Client Response",
            {
                "fields": ("client_notes", "client_decision_date"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created", "modified"),
            },
        ),
    )

