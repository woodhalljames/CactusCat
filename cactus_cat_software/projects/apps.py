from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = "cactus_cat_software.projects"
    verbose_name = _("Projects")

    def ready(self):
        try:
            import cactus_cat_software.projects.signals  # noqa: F401
        except ImportError:
            pass
