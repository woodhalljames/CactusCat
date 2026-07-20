from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CourseCatalogView.as_view(), name="catalog"),
    path("search/", views.CourseSearchView.as_view(), name="search"),
    path("dashboard/", views.StudentDashboardView.as_view(), name="student_dashboard"),
    path("business/apply/", views.BusinessApplyView.as_view(), name="business_apply"),
    path("business/<slug:slug>/", views.BusinessProfileView.as_view(), name="business_profile"),
    path("business/<slug:slug>/comment/", views.PostBusinessCommentView.as_view(), name="business_comment"),
    path("teacher/<slug:slug>/", views.TeacherProfileView.as_view(), name="teacher_profile"),
    path("profile/update/", views.UpdateStudentProfileView.as_view(), name="update_profile"),
    path("profile/photo/", views.UploadProfilePhotoView.as_view(), name="upload_photo"),
    path("profile/<uuid:token>/", views.StudentPublicProfileView.as_view(), name="public_profile"),
    path("certificate/<uuid:cert_id>/", views.CertificateView.as_view(), name="certificate"),
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("<slug:slug>/enroll/", views.EnrollView.as_view(), name="enroll"),
]
