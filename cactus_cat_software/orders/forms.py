from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    """Form for guest and authenticated checkout."""

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "company_name",
            "custom_requirements",
        ]
        widgets = {
            "custom_requirements": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Pre-fill for authenticated users
        if self.user and self.user.is_authenticated:
            self.fields["customer_email"].initial = self.user.email
            self.fields["customer_name"].initial = self.user.name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("customer_name", css_class="form-group col-md-6 mb-3"),
                Column("customer_email", css_class="form-group col-md-6 mb-3"),
            ),
            Row(
                Column("customer_phone", css_class="form-group col-md-6 mb-3"),
                Column("company_name", css_class="form-group col-md-6 mb-3"),
            ),
            "custom_requirements",
            Submit("submit", "Place Order", css_class="btn btn-primary btn-lg"),
        )
