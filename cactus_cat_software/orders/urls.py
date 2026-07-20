from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    # Quote builder (cart)
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:service_id>/", views.CartAddView.as_view(), name="cart_add"),
    path("remove/<int:service_id>/", views.CartRemoveView.as_view(), name="cart_remove"),
    path("request/", views.CartCheckoutView.as_view(), name="cart_checkout"),
    # Single-service checkout
    path("service/<slug:service_slug>/", views.CheckoutView.as_view(), name="checkout"),
    # Post-submission
    path("complete/<str:order_number>/", views.OrderCompleteView.as_view(), name="complete"),
    path("<str:order_number>/", views.OrderDetailView.as_view(), name="detail"),
]
