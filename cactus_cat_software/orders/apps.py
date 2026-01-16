from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    name = "cactus_cat_software.orders"
    verbose_name = _("Orders")

    def ready(self):
        try:
            import cactus_cat_software.orders.signals  # noqa: F401
        except ImportError:
            pass
