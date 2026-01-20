from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectDashboardView.as_view(), name="dashboard"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="detail"),
    path("<int:pk>/add-note/", views.AddProjectNoteView.as_view(), name="add_note"),
    path(
        "<int:pk>/approvals/<int:approval_id>/<str:action>/",
        views.ApprovalActionView.as_view(),
        name="approval_action",
    ),
    # Deployment endpoints
    path(
        "preview/<uuid:token>/",
        views.PreviewRedirectView.as_view(),
        name="preview",
    ),
    path(
        "webhooks/github/<int:project_id>/",
        views.GitHubWebhookView.as_view(),
        name="github_webhook",
    ),
]
