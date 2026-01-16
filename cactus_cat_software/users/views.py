from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, FormView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from cactus_cat_software.users.models import NewsletterSubscriber, User

from .forms import ContactForm
from .tasks import send_contact_form_email


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name", "company_name", "phone_number", "website", "additional_contacts"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return reverse("projects:dashboard")

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("projects:dashboard")


user_redirect_view = UserRedirectView.as_view()


class ContactView(FormView):
    """Contact form view."""

    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Send email asynchronously
        send_contact_form_email.delay(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            subject=form.cleaned_data["subject"],
            message=form.cleaned_data["message"],
        )

        messages.success(
            self.request,
            "Thank you for your message! We'll get back to you soon.",
        )
        return super().form_valid(form)


contact_view = ContactView.as_view()


class NewsletterSubscribeView(CreateView):
    """Newsletter subscription view."""

    model = NewsletterSubscriber
    fields = ["email"]
    template_name = "pages/home.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        try:
            super().form_valid(form)
            success_message = "Thank you for subscribing to our newsletter!"

            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': success_message
                })

            messages.success(self.request, success_message)
            return redirect(self.success_url)
        except Exception:
            info_message = "This email is already subscribed to our newsletter."

            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': info_message
                })

            messages.info(self.request, info_message)
            return redirect(self.success_url)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()
            error_message = "Please provide a valid email address."
            if 'email' in errors:
                error_message = errors['email'][0]['message']
            return JsonResponse({
                'success': False,
                'message': error_message
            })
        return super().form_invalid(form)


newsletter_subscribe_view = NewsletterSubscribeView.as_view()


class NewsletterUnsubscribeView(FormView):
    """Newsletter unsubscribe view."""

    template_name = "pages/newsletter_unsubscribe.html"
    success_url = reverse_lazy("home")

    def get_form_class(self):
        from django import forms
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Submit

        class UnsubscribeForm(forms.Form):
            email = forms.EmailField(
                label="Email Address",
                widget=forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your email address'
                })
            )

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_method = 'post'
                self.helper.add_input(
                    Submit("submit", "Unsubscribe", css_class="btn btn-danger w-100")
                )

        return UnsubscribeForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            subscriber = NewsletterSubscriber.objects.get(email=email)
            subscriber.delete()
            messages.success(
                self.request,
                f"Successfully unsubscribed {email} from our newsletter.",
            )
        except NewsletterSubscriber.DoesNotExist:
            messages.warning(
                self.request,
                f"Email {email} is not subscribed to our newsletter.",
            )
        return super().form_valid(form)


newsletter_unsubscribe_view = NewsletterUnsubscribeView.as_view()
