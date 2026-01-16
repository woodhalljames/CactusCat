import json
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView

from .models import Project, ProjectApproval, ProjectNote


class ProjectDashboardView(LoginRequiredMixin, ListView):
    """Client dashboard showing all their projects."""

    model = Project
    template_name = "projects/dashboard.html"
    context_object_name = "projects"

    def get_queryset(self):
        return (
            Project.objects.filter(client=self.request.user)
            .prefetch_related("updates", "invoices")
            .order_by("-created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user's orders to the context
        from cactus_cat_software.orders.models import Order
        context['orders'] = (
            Order.objects.filter(user=self.request.user)
            .select_related('service_package')
            .prefetch_related('items__service_package')
            .order_by('-created')
        )
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Detailed view of a single project."""

    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user)


class AddProjectNoteView(LoginRequiredMixin, View):
    """AJAX view for adding notes to a project."""

    def post(self, request, pk):
        try:
            # Get the project and verify access
            project = Project.objects.get(pk=pk)

            # Check if user has access to this project
            if project.client != request.user and not request.user.is_staff:
                return JsonResponse(
                    {"success": False, "error": "Access denied"},
                    status=403
                )

            # Handle both JSON and form data
            if request.content_type == "application/json":
                data = json.loads(request.body)
                content = data.get("content", "").strip()
                parent_id = data.get("parent")
                attachment = None
            else:
                content = request.POST.get("content", "").strip()
                parent_id = request.POST.get("parent")
                attachment = request.FILES.get("attachment")

            if not content:
                return JsonResponse(
                    {"success": False, "error": "Content is required"},
                    status=400
                )

            # Create the note
            note = ProjectNote.objects.create(
                project=project,
                author=request.user,
                content=content,
                parent_id=parent_id if parent_id else None,
                attachment=attachment,
            )

            return JsonResponse({
                "success": True,
                "note_id": note.id,
                "message": "Note posted successfully"
            })

        except Project.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Project not found"},
                status=404
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": str(e)},
                status=500
            )


class ApprovalActionView(LoginRequiredMixin, View):
    """Handle client approval actions (approve/reject/revise)."""

    def post(self, request, pk, approval_id, action):
        try:
            # Get the project and approval
            project = Project.objects.get(pk=pk)
            approval = ProjectApproval.objects.get(pk=approval_id, project=project)

            # Check if user has access to this project
            if project.client != request.user:
                return JsonResponse(
                    {"success": False, "error": "Access denied"},
                    status=403
                )

            # Check if approval is still pending
            if approval.status != "pending":
                return JsonResponse(
                    {"success": False, "error": "This approval has already been responded to"},
                    status=400
                )

            # Parse request data
            data = json.loads(request.body)
            client_notes = data.get("client_notes", "").strip()

            # Map action to status
            status_map = {
                "approve": "approved",
                "reject": "rejected",
                "revise": "revised",
            }

            if action not in status_map:
                return JsonResponse(
                    {"success": False, "error": "Invalid action"},
                    status=400
                )

            # Update approval
            approval.status = status_map[action]
            approval.client_notes = client_notes
            approval.client_decision_date = timezone.now()
            approval.save()

            return JsonResponse({
                "success": True,
                "message": f"Approval {action}d successfully",
                "status": approval.status
            })

        except Project.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Project not found"},
                status=404
            )
        except ProjectApproval.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Approval not found"},
                status=404
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": str(e)},
                status=500
            )
