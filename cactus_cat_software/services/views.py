from django.views.generic import DetailView, ListView

from .models import ServiceCategory, ServicePackage


class ServiceCatalogView(ListView):
    """Display all active service packages grouped by category."""

    model = ServicePackage
    template_name = "services/catalog.html"
    context_object_name = "packages"

    def get_queryset(self):
        return (
            ServicePackage.objects.filter(
                is_active=True,
                category__is_active=True,
            )
            .select_related("category")
            .order_by("category__display_order", "display_order")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            ServiceCategory.objects.filter(is_active=True)
            .prefetch_related("packages")
            .order_by("display_order")
        )
        return context


class ServiceDetailView(DetailView):
    """Display individual service package details."""

    model = ServicePackage
    template_name = "services/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return ServicePackage.objects.filter(is_active=True)
