from django.contrib import admin, messages

from .models import (
    Business,
    BusinessApplication,
    BusinessComment,
    BusinessLocation,
    Course,
    Enrollment,
    StudentProfile,
    Teacher,
)


class TeacherInline(admin.TabularInline):
    model = Teacher
    extra = 1
    fields = ["name", "title", "email", "url", "location"]


class BusinessLocationInline(admin.TabularInline):
    model = BusinessLocation
    extra = 1
    fields = ["name", "city", "state", "is_active"]


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "owner", "is_active", "teacher_count", "course_count", "location_count"]
    list_filter = ["is_active"]
    search_fields = ["name", "owner__email"]
    raw_id_fields = ["owner"]
    inlines = [BusinessLocationInline, TeacherInline]

    def teacher_count(self, obj):
        return obj.teachers.count()
    teacher_count.short_description = "Teachers"

    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = "Courses"

    def location_count(self, obj):
        return obj.locations.count()
    location_count.short_description = "Locations"


@admin.register(BusinessLocation)
class BusinessLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "business", "city", "state", "is_active"]
    list_filter = ["is_active", "business"]
    search_fields = ["name", "business__name", "city"]


def _approve_application(modeladmin, request, queryset):
    """Approve selected business applications."""
    from cactus_cat_software.courses.models import Business

    approved = 0
    for app in queryset.filter(status=BusinessApplication.STATUS_PENDING):
        business, _ = Business.objects.get_or_create(
            name=app.business_name,
            defaults={"url": app.business_url, "description": app.description, "owner": app.user},
        )
        if business.owner is None:
            business.owner = app.user
            business.save(update_fields=["owner"])

        app.status = BusinessApplication.STATUS_APPROVED
        app.linked_business = business
        app.save(update_fields=["status", "linked_business"])

        user = app.user
        user.account_type = "business"
        user.company_name = app.business_name
        user.website = app.business_url
        user.save(update_fields=["account_type", "company_name", "website"])
        approved += 1

    modeladmin.message_user(
        request,
        f"{approved} application(s) approved and business account(s) created.",
        level=messages.SUCCESS,
    )

_approve_application.short_description = "Approve selected applications"


def _reject_application(modeladmin, request, queryset):
    """Reject selected business applications."""
    updated = queryset.filter(status=BusinessApplication.STATUS_PENDING).update(
        status=BusinessApplication.STATUS_REJECTED
    )
    for app in queryset.filter(status=BusinessApplication.STATUS_REJECTED):
        if app.user.account_type == "business_applicant":
            app.user.account_type = "student"
            app.user.save(update_fields=["account_type"])

    modeladmin.message_user(
        request,
        f"{updated} application(s) rejected.",
        level=messages.WARNING,
    )

_reject_application.short_description = "Reject selected applications"


@admin.register(BusinessApplication)
class BusinessApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "business_name", "user", "status", "is_google_verified",
        "linked_business", "created",
    ]
    list_filter = ["status", "is_google_verified"]
    search_fields = ["business_name", "user__email"]
    readonly_fields = ["user", "is_google_verified", "created", "modified"]
    raw_id_fields = []
    actions = [_approve_application, _reject_application]

    fieldsets = [
        ("Applicant", {"fields": ["user", "is_google_verified"]}),
        ("Business Info", {"fields": ["business_name", "business_url", "description", "google_profile_url"]}),
        ("Review", {"fields": ["status", "admin_notes", "linked_business"]}),
        ("Timestamps", {"fields": ["created", "modified"], "classes": ["collapse"]}),
    ]


@admin.register(BusinessComment)
class BusinessCommentAdmin(admin.ModelAdmin):
    list_display = ["author", "business", "is_visible", "created"]
    list_filter = ["is_visible", "business"]
    search_fields = ["author__email", "business__name", "body"]
    readonly_fields = ["author", "business", "created"]
    actions = ["hide_comments"]

    def hide_comments(self, request, queryset):
        queryset.update(is_visible=False)
        self.message_user(request, f"{queryset.count()} comment(s) hidden.")
    hide_comments.short_description = "Hide selected comments"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "business", "location", "email"]
    list_filter = ["business"]
    search_fields = ["name", "business__name"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "business", "location", "teacher_list", "is_open", "is_active", "enrollment_count"]
    list_filter = ["is_open", "is_active", "business"]
    search_fields = ["title", "business__name"]
    filter_horizontal = ["teachers"]
    prepopulated_fields = {"slug": ("title",)}

    def teacher_list(self, obj):
        names = list(obj.teachers.values_list("name", flat=True))
        return ", ".join(names) if names else "— none assigned"
    teacher_list.short_description = "Teachers"

    def enrollment_count(self, obj):
        return obj.enrollments.count()
    enrollment_count.short_description = "Enrolled"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_open and not obj.teachers.exists():
            obj.is_open = False
            obj.save(update_fields=["is_open"])
            self.message_user(
                request,
                "Registration was not opened — no teachers are assigned to this course.",
                level=messages.WARNING,
            )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "is_completed", "completed_date", "created"]
    list_filter = ["is_completed", "course__business", "course"]
    search_fields = ["student__email", "course__title"]
    raw_id_fields = ["student"]
    date_hierarchy = "created"
    readonly_fields = ["certificate_id"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["certificate_id", "student", "course"]
        return ["certificate_id"]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "get_display_name", "is_public", "created"]
    list_filter = ["is_public"]
    search_fields = ["user__email", "display_name"]
    readonly_fields = ["share_token"]
