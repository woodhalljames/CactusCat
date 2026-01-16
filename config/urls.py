from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from cactus_cat_software.users import views as user_views

urlpatterns = [
    # Pages
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("contact/", user_views.contact_view, name="contact"),
    path(
        "newsletter/subscribe/",
        user_views.newsletter_subscribe_view,
        name="newsletter_subscribe",
    ),
    path(
        "newsletter/unsubscribe/",
        user_views.newsletter_unsubscribe_view,
        name="newsletter_unsubscribe",
    ),
    # Apps
    path("services/", include("cactus_cat_software.services.urls", namespace="services")),
    path("blog/", include("cactus_cat_software.blog.urls", namespace="blog")),
    path("orders/", include("cactus_cat_software.orders.urls", namespace="orders")),
    path("projects/", include("cactus_cat_software.projects.urls", namespace="projects")),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("cactus_cat_software.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Summernote
    path("summernote/", include("django_summernote.urls")),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            *urlpatterns,
        ]
