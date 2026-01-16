from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServicesConfig(AppConfig):
    name = "cactus_cat_software.services"
    verbose_name = _("Services")

    def ready(self):
        try:
            import cactus_cat_software.services.signals  # noqa: F401
        except ImportError:
            pass
