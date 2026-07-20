from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectDashboardView.as_view(), name="dashboard"),
    path("<slug:service_slug>/<str:order_number>/", views.ProjectDetailView.as_view(), name="detail"),
    path("<int:pk>/add-note/", views.AddProjectNoteView.as_view(), name="add_note"),
    path("<int:pk>/notes/<int:note_id>/edit/", views.EditNoteView.as_view(), name="edit_note"),
    path("<int:pk>/questions/<int:question_id>/answer/", views.AnswerQuestionView.as_view(), name="answer_question"),
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
