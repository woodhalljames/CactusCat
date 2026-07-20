from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("", views.ServiceCatalogView.as_view(), name="catalog"),
    path("quote/", views.QuoteRequestView.as_view(), name="quote"),
    path("<slug:slug>/", views.ServiceDetailView.as_view(), name="detail"),
]
