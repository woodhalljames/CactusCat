from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView

from cactus_cat_software.services.models import ServicePackage

from .cart import Cart
from .forms import CheckoutForm
from .models import Order
from .tasks import send_order_confirmation_email


class CheckoutView(CreateView):
    """Checkout view supporting both guest and authenticated users."""

    model = Order
    form_class = CheckoutForm
    template_name = "orders/checkout.html"

    def dispatch(self, request, *args, **kwargs):
        # Get service package from URL
        self.service_package = get_object_or_404(
            ServicePackage,
            slug=kwargs["service_slug"],
            is_active=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Set order details
        form.instance.service_package = self.service_package
        form.instance.total_amount = self.service_package.price

        # Link to user if authenticated
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user

        response = super().form_valid(form)

        # Send confirmation email asynchronously
        send_order_confirmation_email.delay(self.object.id)

        messages.success(
            self.request,
            f"Quote request sent! Check {form.instance.customer_email} for confirmation.",
        )

        return response

    def get_success_url(self):
        return reverse(
            "orders:complete",
            kwargs={"order_number": self.object.order_number},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service"] = self.service_package
        return context


class OrderCompleteView(DetailView):
    """Thank you page after order is placed."""

    model = Order
    template_name = "orders/order_complete.html"
    context_object_name = "order"
    slug_field = "order_number"
    slug_url_kwarg = "order_number"


class OrderDetailView(DetailView):
    """View order details by order number."""

    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"
    slug_field = "order_number"
    slug_url_kwarg = "order_number"


class CartAddView(View):
    """Add a service to the cart."""

    def post(self, request, service_id):
        cart = Cart(request)
        service = get_object_or_404(ServicePackage, id=service_id, is_active=True)
        already_in_cart = str(service.id) in cart.cart
        cart.add(service_package=service, quantity=1, override_quantity=False)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if already_in_cart:
                return JsonResponse({
                    'success': True,
                    'cart_count': len(cart),
                    'message': f'{service.name} is already in your quote'
                })
            return JsonResponse({
                'success': True,
                'cart_count': len(cart),
                'message': f'{service.name} added to quote'
            })

        if already_in_cart:
            messages.info(request, f'{service.name} is already in your quote')
        else:
            messages.success(request, f'{service.name} added to quote')
        return redirect('orders:cart_detail')


class CartRemoveView(View):
    """Remove a service from the cart."""

    def post(self, request, service_id):
        cart = Cart(request)
        service = get_object_or_404(ServicePackage, id=service_id)
        cart.remove(service_package=service)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': len(cart),
                'message': 'Item removed from cart'
            })

        messages.success(request, 'Item removed from cart')
        return redirect('orders:cart_detail')


class CartDetailView(View):
    """Display the cart."""

    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart_detail.html', {'cart': cart})


class CartCheckoutView(CreateView):
    """Checkout view for cart-based orders."""

    model = Order
    form_class = CheckoutForm
    template_name = "orders/cart_checkout.html"

    def dispatch(self, request, *args, **kwargs):
        # Ensure cart is not empty
        self.cart = Cart(request)
        if len(self.cart) == 0:
            messages.warning(request, "Your cart is empty.")
            return redirect('orders:cart_detail')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        from decimal import Decimal
        from .models import OrderItem

        # Create the order
        form.instance.total_amount = self.cart.get_total_price()

        # Link to user if authenticated
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user

        # Save order first (without service_package since it's now optional)
        self.object = form.save()

        # Create order items from cart
        for item in self.cart:
            OrderItem.objects.create(
                order=self.object,
                service_package=item['service'],
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear the cart
        self.cart.clear()

        # Send confirmation emails asynchronously
        send_order_confirmation_email.delay(self.object.id)

        messages.success(
            self.request,
            f"Quote request sent! Check {form.instance.customer_email} for confirmation.",
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "orders:complete",
            kwargs={"order_number": self.object.order_number},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = self.cart
        return context
