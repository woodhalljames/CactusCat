from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    # Cart
    path("cart/", views.CartDetailView.as_view(), name="cart_detail"),
    path("cart/add/<int:service_id>/", views.CartAddView.as_view(), name="cart_add"),
    path("cart/remove/<int:service_id>/", views.CartRemoveView.as_view(), name="cart_remove"),
    path("cart/checkout/", views.CartCheckoutView.as_view(), name="cart_checkout"),
    # Checkout
    path(
        "checkout/<slug:service_slug>/",
        views.CheckoutView.as_view(),
        name="checkout",
    ),
    path(
        "complete/<str:order_number>/",
        views.OrderCompleteView.as_view(),
        name="complete",
    ),
    path(
        "<str:order_number>/",
        views.OrderDetailView.as_view(),
        name="detail",
    ),
]
