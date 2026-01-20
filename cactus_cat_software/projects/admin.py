from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Project,
    ProjectApproval,
    ProjectDeployment,
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


class ProjectDeploymentInline(admin.StackedInline):
    model = ProjectDeployment
    extra = 0
    max_num = 1
    fields = [
        "github_repo_url",
        "github_branch",
        "status",
        "internal_port",
        "memory_limit",
        "cpu_limit",
    ]
    readonly_fields = ["status"]


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
        ProjectDeploymentInline,
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


@admin.register(ProjectDeployment)
class ProjectDeploymentAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "status_badge",
        "github_repo_url",
        "github_branch",
        "last_deployed_at",
        "deployment_actions",
    ]
    list_filter = ["status", "last_deployed_at", "created"]
    search_fields = ["project__project_name", "github_repo_url", "project__slug"]
    readonly_fields = [
        "status",
        "container_id",
        "image_name",
        "preview_token",
        "webhook_secret",
        "last_deployed_at",
        "build_log_display",
        "preview_url_display",
        "webhook_url_display",
        "client_preview_link",
        "created",
        "modified",
    ]
    actions = ["deploy_selected", "stop_selected", "redeploy_selected"]

    fieldsets = (
        (
            "Project",
            {
                "fields": ("project",),
            },
        ),
        (
            "GitHub Configuration",
            {
                "fields": (
                    "github_repo_url",
                    "github_branch",
                    "webhook_secret",
                    "webhook_url_display",
                ),
            },
        ),
        (
            "Container Settings",
            {
                "fields": (
                    "internal_port",
                    "memory_limit",
                    "cpu_limit",
                ),
            },
        ),
        (
            "Deployment Status",
            {
                "fields": (
                    "status",
                    "container_id",
                    "image_name",
                    "last_deployed_at",
                ),
            },
        ),
        (
            "Preview Access",
            {
                "fields": (
                    "preview_token",
                    "preview_url_display",
                    "client_preview_link",
                ),
                "description": "Share the 'Client Preview Link' with your client so they can access their preview.",
            },
        ),
        (
            "Build Log",
            {
                "fields": ("build_log_display",),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created", "modified"),
                "classes": ("collapse",),
            },
        ),
    )

    def status_badge(self, obj):
        """Display status as a colored badge."""
        colors = {
            "pending": "#6c757d",
            "cloning": "#17a2b8",
            "building": "#17a2b8",
            "starting": "#17a2b8",
            "running": "#28a745",
            "stopped": "#ffc107",
            "failed": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display(),
        )
    status_badge.short_description = "Status"

    def deployment_actions(self, obj):
        """Display action buttons based on current status."""
        from django.urls import reverse

        buttons = []

        if obj.can_deploy():
            deploy_url = reverse("admin:projects_projectdeployment_deploy", args=[obj.pk])
            buttons.append(
                f'<a class="button" style="background: #28a745; color: white; padding: 5px 10px; '
                f'text-decoration: none; border-radius: 3px; margin-right: 5px;" '
                f'href="{deploy_url}">Deploy</a>'
            )

        if obj.can_stop():
            stop_url = reverse("admin:projects_projectdeployment_stop", args=[obj.pk])
            buttons.append(
                f'<a class="button" style="background: #dc3545; color: white; padding: 5px 10px; '
                f'text-decoration: none; border-radius: 3px; margin-right: 5px;" '
                f'href="{stop_url}">Stop</a>'
            )

        if obj.is_running():
            redeploy_url = reverse("admin:projects_projectdeployment_redeploy", args=[obj.pk])
            buttons.append(
                f'<a class="button" style="background: #17a2b8; color: white; padding: 5px 10px; '
                f'text-decoration: none; border-radius: 3px;" '
                f'href="{redeploy_url}">Redeploy</a>'
            )

        if obj.is_deploying():
            buttons.append(
                '<span style="color: #17a2b8; font-style: italic;">Deploying...</span>'
            )

        return format_html(" ".join(buttons)) if buttons else "-"
    deployment_actions.short_description = "Actions"

    def build_log_display(self, obj):
        """Display build log in a scrollable pre-formatted box."""
        if not obj.build_log:
            return "No build log available"
        return format_html(
            '<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; '
            'border-radius: 5px; max-height: 400px; overflow-y: auto; '
            'font-family: monospace; font-size: 12px; white-space: pre-wrap;">{}</pre>',
            obj.build_log,
        )
    build_log_display.short_description = "Build Log"

    def preview_url_display(self, obj):
        """Display the Traefik route path."""
        if obj.is_running():
            url = obj.get_preview_url()
            return format_html(
                '<code style="background: #e9ecef; padding: 5px 10px; border-radius: 3px;">{}</code>',
                url,
            )
        return "Container not running"
    preview_url_display.short_description = "Preview Path"

    def webhook_url_display(self, obj):
        """Display the webhook URL for GitHub."""
        if obj.pk:
            url = obj.get_webhook_url()
            return format_html(
                '<code style="background: #e9ecef; padding: 5px 10px; border-radius: 3px; '
                'word-break: break-all;">{}</code><br>'
                '<small class="text-muted">Add this URL as a webhook in your GitHub repo settings. '
                'Use Content-Type: application/json and the secret shown above.</small>',
                url,
            )
        return "Save first to generate webhook URL"
    webhook_url_display.short_description = "Webhook URL"

    def client_preview_link(self, obj):
        """Display the link to share with clients."""
        if obj.pk:
            url = obj.get_preview_link()
            return format_html(
                '<a href="{}" target="_blank" style="background: #007bff; color: white; '
                'padding: 8px 15px; text-decoration: none; border-radius: 5px; '
                'display: inline-block;">'
                'Open Client Preview Link</a><br>'
                '<small class="text-muted">Share this link with your client. '
                'They will be redirected to the live preview when the container is running.</small>',
                url,
            )
        return "Save first to generate preview link"
    client_preview_link.short_description = "Client Preview Link"

    def get_urls(self):
        """Add custom admin URLs for deploy/stop/redeploy actions."""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:pk>/deploy/",
                self.admin_site.admin_view(self.deploy_view),
                name="projects_projectdeployment_deploy",
            ),
            path(
                "<int:pk>/stop/",
                self.admin_site.admin_view(self.stop_view),
                name="projects_projectdeployment_stop",
            ),
            path(
                "<int:pk>/redeploy/",
                self.admin_site.admin_view(self.redeploy_view),
                name="projects_projectdeployment_redeploy",
            ),
        ]
        return custom_urls + urls

    def deploy_view(self, request, pk):
        """Handle deploy button click."""
        from django.contrib import messages
        from django.shortcuts import redirect

        from .tasks import build_and_deploy

        deployment = self.get_object(request, pk)
        if deployment and deployment.can_deploy():
            build_and_deploy.delay(deployment.id)
            messages.success(
                request,
                f"Deployment started for {deployment.project.project_name}. "
                "Check the build log for progress.",
            )
        else:
            messages.error(request, "Cannot deploy - deployment is already in progress or running.")

        return redirect("admin:projects_projectdeployment_change", pk)

    def stop_view(self, request, pk):
        """Handle stop button click."""
        from django.contrib import messages
        from django.shortcuts import redirect

        from .tasks import stop_deployment

        deployment = self.get_object(request, pk)
        if deployment and deployment.can_stop():
            stop_deployment.delay(deployment.id)
            messages.success(
                request,
                f"Stop command sent for {deployment.project.project_name}.",
            )
        else:
            messages.error(request, "Cannot stop - container is not running.")

        return redirect("admin:projects_projectdeployment_change", pk)

    def redeploy_view(self, request, pk):
        """Handle redeploy button click."""
        from django.contrib import messages
        from django.shortcuts import redirect

        from .tasks import build_and_deploy, stop_deployment

        deployment = self.get_object(request, pk)
        if deployment:
            # Stop first, then deploy
            if deployment.container_id:
                stop_deployment.delay(deployment.id)
            build_and_deploy.apply_async((deployment.id,), countdown=5)  # Wait 5s for stop
            messages.success(
                request,
                f"Redeploy started for {deployment.project.project_name}.",
            )
        else:
            messages.error(request, "Deployment not found.")

        return redirect("admin:projects_projectdeployment_change", pk)

    @admin.action(description="Deploy selected deployments")
    def deploy_selected(self, request, queryset):
        from django.contrib import messages

        from .tasks import build_and_deploy

        count = 0
        for deployment in queryset:
            if deployment.can_deploy():
                build_and_deploy.delay(deployment.id)
                count += 1

        messages.success(request, f"Started deployment for {count} project(s).")

    @admin.action(description="Stop selected deployments")
    def stop_selected(self, request, queryset):
        from django.contrib import messages

        from .tasks import stop_deployment

        count = 0
        for deployment in queryset:
            if deployment.can_stop():
                stop_deployment.delay(deployment.id)
                count += 1

        messages.success(request, f"Sent stop command for {count} project(s).")

    @admin.action(description="Redeploy selected deployments")
    def redeploy_selected(self, request, queryset):
        from django.contrib import messages

        from .tasks import build_and_deploy, stop_deployment

        count = 0
        for deployment in queryset:
            if deployment.container_id:
                stop_deployment.delay(deployment.id)
            build_and_deploy.apply_async((deployment.id,), countdown=5)
            count += 1

        messages.success(request, f"Started redeploy for {count} project(s).")
