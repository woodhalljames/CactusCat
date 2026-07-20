import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from .models import Business, BusinessApplication, BusinessComment, Course, Enrollment, StudentProfile, Teacher


class CourseCatalogView(ListView):
    """Public listing of all open courses."""

    template_name = "courses/catalog.html"
    context_object_name = "courses"
    paginate_by = 24

    def get_queryset(self):
        qs = (
            Course.objects.filter(is_open=True, is_active=True)
            .select_related("business")
            .prefetch_related("teachers")
            .order_by("business__name", "title")
        )
        biz = self.request.GET.get("business")
        if biz:
            qs = qs.filter(business__id=biz)
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(business__name__icontains=q) |
                Q(skills__icontains=q) |
                Q(description__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["businesses"] = Business.objects.filter(is_active=True).order_by("name")
        context["selected_business"] = self.request.GET.get("business", "")
        context["search_query"] = self.request.GET.get("q", "")
        context["is_landing"] = not self.request.GET.get("q") and not self.request.GET.get("business") and not self.request.GET.get("page")
        context["featured_courses"] = (
            Course.objects.filter(is_open=True, is_active=True)
            .select_related("business")
            .prefetch_related("teachers")
            .order_by("?")[:6]
        )
        if self.request.user.is_authenticated:
            context["enrolled_course_ids"] = set(
                self.request.user.enrollments.values_list("course_id", flat=True)
            )
        else:
            context["enrolled_course_ids"] = set()
        return context


class CourseSearchView(View):
    """AJAX — returns up to 8 matching open courses as JSON for the home page search."""

    def get(self, request):
        q = request.GET.get("q", "").strip()
        if len(q) < 2:
            return JsonResponse({"results": []})
        courses = (
            Course.objects.filter(
                is_open=True, is_active=True,
            ).filter(
                Q(title__icontains=q) |
                Q(business__name__icontains=q) |
                Q(skills__icontains=q)
            )
            .select_related("business")
            .prefetch_related("teachers")[:8]
        )
        results = []
        for c in courses:
            results.append({
                "title": c.title,
                "business": c.business.name,
                "business_url": c.business.get_absolute_url(),
                "skills": c.get_skills_list()[:4],
                "url": f"/courses/{c.slug}/",
                "logo_url": c.business.logo.url if c.business.logo else None,
            })
        return JsonResponse({"results": results, "total": Course.objects.filter(
            is_open=True, is_active=True,
        ).filter(
            Q(title__icontains=q) |
            Q(business__name__icontains=q) |
            Q(skills__icontains=q)
        ).count()})


class CourseDetailView(DetailView):
    """Public course detail page with enroll button."""

    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        return (
            Course.objects.filter(is_active=True)
            .select_related("business")
            .prefetch_related("teachers")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["enrollment"] = Enrollment.objects.filter(
                student=self.request.user, course=self.object
            ).first()
        return context


class EnrollView(LoginRequiredMixin, View):
    """POST — enroll the current user in a course."""

    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_open=True, is_active=True)
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user, course=course
        )
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "created": created,
                "message": "Enrolled!" if created else "Already enrolled.",
            })
        return redirect("courses:student_dashboard")


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    """Authenticated student's own control panel."""

    template_name = "courses/student_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        enrollments = (
            self.request.user.enrollments
            .select_related("course", "course__business")
            .prefetch_related("course__teachers")
            .order_by("-completed_date", "-created")
        )
        context["profile"] = profile
        context["enrollments"] = enrollments
        context["completed_count"] = enrollments.filter(is_completed=True).count()
        context["public_url"] = self.request.build_absolute_uri(profile.get_public_url())
        return context


class UpdateStudentProfileView(LoginRequiredMixin, View):
    """AJAX — saves display name, bio, and privacy toggle."""

    def post(self, request):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            data = request.POST

        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        profile.display_name = data.get("display_name", profile.display_name).strip()
        profile.bio = data.get("bio", profile.bio).strip()
        profile.is_public = bool(data.get("is_public", profile.is_public))
        profile.save()
        return JsonResponse({
            "success": True,
            "is_public": profile.is_public,
            "display_name": profile.get_display_name(),
        })


class UploadProfilePhotoView(LoginRequiredMixin, View):
    """AJAX multipart — saves profile photo."""

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        photo = request.FILES.get("photo")
        if not photo:
            return JsonResponse({"success": False, "error": "No file provided"}, status=400)
        if photo.size > 5 * 1024 * 1024:
            return JsonResponse({"success": False, "error": "File must be under 5 MB"}, status=400)
        if not photo.content_type.startswith("image/"):
            return JsonResponse({"success": False, "error": "File must be an image"}, status=400)
        if profile.profile_photo:
            profile.profile_photo.delete(save=False)
        profile.profile_photo = photo
        profile.save(update_fields=["profile_photo"])
        return JsonResponse({"success": True, "photo_url": profile.profile_photo.url})


class StudentPublicProfileView(TemplateView):
    """Public shareable profile — no authentication required."""

    template_name = "courses/public_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(StudentProfile, share_token=self.kwargs["token"])
        context["profile"] = profile
        if profile.is_public:
            context["enrollments"] = profile.completed_enrollments()
        return context


class CertificateView(TemplateView):
    """Public printable certificate — no authentication required."""

    template_name = "courses/certificate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = get_object_or_404(
            Enrollment.objects.select_related("student", "course", "course__business")
            .prefetch_related("course__teachers"),
            certificate_id=self.kwargs["cert_id"],
            is_completed=True,
        )
        profile = StudentProfile.objects.filter(user=enrollment.student).first()
        display_name = profile.get_display_name() if profile else enrollment.student.email.split("@")[0]
        context["enrollment"] = enrollment
        context["display_name"] = display_name
        return context


class BusinessApplyView(LoginRequiredMixin, View):
    """Submit or update a business application."""

    template_name = "courses/business_apply.html"

    def _get_or_none(self, request):
        try:
            return request.user.business_application
        except BusinessApplication.DoesNotExist:
            return None

    def get(self, request):
        application = self._get_or_none(request)
        is_already_business = request.user.account_type == "business"
        return render(request, self.template_name, {
            "application": application,
            "is_already_business": is_already_business,
        })

    def post(self, request):
        application = self._get_or_none(request)

        if request.user.account_type == "business":
            messages.info(request, "Your account is already a verified business account.")
            return redirect("courses:business_apply")

        business_name = request.POST.get("business_name", "").strip()
        business_url = request.POST.get("business_url", "").strip()
        description = request.POST.get("description", "").strip()
        google_profile_url = request.POST.get("google_profile_url", "").strip()

        if not business_name:
            messages.error(request, "Business name is required.")
            return render(request, self.template_name, {"application": application, "is_already_business": False})

        is_google_verified = False
        try:
            from allauth.socialaccount.models import SocialAccount
            is_google_verified = SocialAccount.objects.filter(
                user=request.user, provider="google"
            ).exists()
        except Exception:
            pass

        if application and application.status == BusinessApplication.STATUS_PENDING:
            application.business_name = business_name
            application.business_url = business_url
            application.description = description
            application.google_profile_url = google_profile_url
            application.is_google_verified = is_google_verified
            application.save()
            messages.success(request, "Your application has been updated.")
        elif application and application.status == BusinessApplication.STATUS_APPROVED:
            messages.info(request, "Your application has already been approved.")
        elif application and application.status == BusinessApplication.STATUS_REJECTED:
            application.status = BusinessApplication.STATUS_PENDING
            application.business_name = business_name
            application.business_url = business_url
            application.description = description
            application.google_profile_url = google_profile_url
            application.is_google_verified = is_google_verified
            application.admin_notes = ""
            application.save()
            messages.success(request, "Your application has been resubmitted for review.")
        else:
            BusinessApplication.objects.create(
                user=request.user,
                business_name=business_name,
                business_url=business_url,
                description=description,
                google_profile_url=google_profile_url,
                is_google_verified=is_google_verified,
            )
            request.user.account_type = "business_applicant"
            request.user.save(update_fields=["account_type"])
            messages.success(request, "Your business application has been submitted. We'll review it shortly.")

        return redirect("courses:business_apply")


class BusinessProfileView(DetailView):
    """Public business profile page — open to anyone."""

    model = Business
    template_name = "courses/business_profile.html"
    context_object_name = "business"

    def get_queryset(self):
        return (
            Business.objects.filter(is_active=True)
            .prefetch_related("locations", "teachers", "courses")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        biz = self.object
        context["courses"] = (
            biz.courses.filter(is_open=True, is_active=True)
            .prefetch_related("teachers")
        )
        context["locations"] = biz.locations.filter(is_active=True)
        context["teachers"] = biz.teachers.all()
        context["comments"] = (
            biz.comments.filter(is_visible=True)
            .select_related("author", "author__student_profile")
            .order_by("-created")[:50]
        )
        context["user_already_commented"] = (
            self.request.user.is_authenticated and
            biz.comments.filter(author=self.request.user, is_visible=True).exists()
        )
        return context


class PostBusinessCommentView(LoginRequiredMixin, View):
    """AJAX — post a comment on a business profile."""

    def post(self, request, slug):
        business = get_object_or_404(Business, slug=slug, is_active=True)
        body = request.POST.get("body", "").strip()
        if not body:
            return JsonResponse({"success": False, "error": "Comment cannot be empty"}, status=400)
        if len(body) > 1000:
            return JsonResponse({"success": False, "error": "Comment too long (max 1000 characters)"}, status=400)

        comment, created = BusinessComment.objects.get_or_create(
            business=business,
            author=request.user,
            defaults={"body": body},
        )
        if not created:
            comment.body = body
            comment.is_visible = True
            comment.save(update_fields=["body", "is_visible"])

        profile = getattr(request.user, "student_profile", None)
        display_name = profile.get_display_name() if profile else request.user.email.split("@")[0]
        photo_url = profile.profile_photo.url if profile and profile.profile_photo else None

        return JsonResponse({
            "success": True,
            "comment": {
                "body": comment.body,
                "author": display_name,
                "photo_url": photo_url,
                "date": comment.created.strftime("%b %d, %Y"),
            },
        })


class TeacherProfileView(DetailView):
    """Public teacher profile — always discoverable."""

    model = Teacher
    template_name = "courses/teacher_profile.html"
    context_object_name = "teacher"

    def get_queryset(self):
        return Teacher.objects.select_related("business", "location").prefetch_related("courses")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = (
            self.object.courses.filter(is_active=True)
            .select_related("business")
            .order_by("-is_open", "title")
        )
        return context
