from django.contrib import admin

from .models import (
    Project,
    ProjectApproval,
    ProjectInvoice,
    ProjectItem,
    ProjectMilestone,
    ProjectNote,
    ProjectUpdate,
)


class ProjectUpdateInline(admin.TabularInline):
    model = ProjectUpdate
    extra = 0
    fields = ["title", "image", "requires_approval", "approved", "created"]
    readonly_fields = ["created"]


class ProjectInvoiceInline(admin.TabularInline):
    model = ProjectInvoice
    extra = 0
    fields = ["invoice_number", "amount", "due_date", "status", "paid_date"]


class ProjectItemInline(admin.TabularInline):
    model = ProjectItem
    extra = 0
    fields = ["name", "status", "progress_percentage", "display_order", "due_date"]
    ordering = ["display_order", "created"]


class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    extra = 0
    fields = ["name", "status", "display_order", "target_date", "completion_date"]
    ordering = ["display_order", "target_date"]


class ProjectNoteInline(admin.StackedInline):
    model = ProjectNote
    extra = 0
    fields = ["author", "content", "item", "attachment", "is_internal", "parent"]
    readonly_fields = ["created"]


class ProjectApprovalInline(admin.TabularInline):
    model = ProjectApproval
    extra = 0
    fields = ["title", "status", "requires_response", "document", "created"]
    readonly_fields = ["created"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "project_name",
        "slug",
        "client",
        "status",
        "progress_percentage",
        "estimated_completion",
    ]
    list_filter = ["status", "created"]
    search_fields = ["project_name", "slug", "client__email", "order__order_number"]
    readonly_fields = ["slug"]
    prepopulated_fields = {"slug": ("project_name",)}
    inlines = [
        ProjectItemInline,
        ProjectMilestoneInline,
        ProjectApprovalInline,
        ProjectUpdateInline,
        ProjectInvoiceInline,
        ProjectNoteInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("order", "client", "project_name", "slug"),
            },
        ),
        (
            "Status",
            {
                "fields": ("status", "progress_percentage", "status_notes"),
            },
        ),
        (
            "Timeline",
            {
                "fields": ("estimated_completion", "actual_completion"),
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


@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "project",
        "status",
        "progress_percentage",
        "due_date",
        "display_order",
    ]
    list_filter = ["status", "created", "due_date"]
    search_fields = ["name", "project__project_name", "description"]
    list_editable = ["status", "progress_percentage", "display_order"]


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


@admin.register(ProjectMilestone)
class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "project",
        "status",
        "target_date",
        "completion_date",
        "display_order",
    ]
    list_filter = ["status", "target_date", "completion_date"]
    search_fields = ["name", "project__project_name", "description"]
    list_editable = ["status", "display_order"]


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
                "fields": ("project", "title", "description", "document"),
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
