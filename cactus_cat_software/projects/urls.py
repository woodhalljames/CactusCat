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
]
