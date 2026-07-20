from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from .forms import QuoteRequestForm
from .models import ServiceCategory, ServicePackage
from .tasks import send_quote_request_email


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote_form"] = QuoteRequestForm(
            initial={"service_name": self.object.name}
        )
        return context


class QuoteRequestView(View):
    """Handle AJAX quote request form submission."""

    def post(self, request, *args, **kwargs):
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            send_quote_request_email.delay(
                name=data["name"],
                email=data["email"],
                service_name=data["service_name"],
                budget_range=data["budget_range"],
                goals=data["goals"],
                timeline=data["timeline"],
            )
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)
