from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, FormView, View
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from cactus_cat_software.users.models import AccountInvite, NewsletterSubscriber, User

from .forms import BusinessInfoForm, InviteForm
from .tasks import send_invite_email


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name", "company_name", "phone_number", "website"]
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


class UpdateBusinessInfoView(LoginRequiredMixin, View):
    """Inline AJAX update of business info from the dashboard."""

    def post(self, request):
        form = BusinessInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


update_business_info_view = UpdateBusinessInfoView.as_view()


class SendInviteView(LoginRequiredMixin, View):
    """Send a team invite email."""

    def post(self, request):
        form = InviteForm(request.user, request.POST)
        if not form.is_valid():
            errors = {f: e[0] for f, e in form.errors.items()}
            return JsonResponse({"success": False, "error": errors.get("email", "Invalid email.")}, status=400)

        email = form.cleaned_data["email"]
        invite, _ = AccountInvite.objects.get_or_create(
            inviter=request.user,
            email=email,
            defaults={"accepted": False},
        )

        accept_url = request.build_absolute_uri(
            reverse("users:accept_invite", kwargs={"token": invite.token})
        )
        send_invite_email.delay(invite.id, accept_url)

        return JsonResponse({
            "success": True,
            "invite": {
                "id": invite.id,
                "email": invite.email,
                "accepted": invite.accepted,
            },
        })


send_invite_view = SendInviteView.as_view()


class RevokeInviteView(LoginRequiredMixin, View):
    """Revoke a pending invite."""

    def post(self, request, invite_id):
        invite = get_object_or_404(AccountInvite, pk=invite_id, inviter=request.user, accepted=False)
        invite.delete()
        return JsonResponse({"success": True})


revoke_invite_view = RevokeInviteView.as_view()


class RemoveTeamMemberView(LoginRequiredMixin, View):
    """Remove an accepted team member and revoke project access."""

    def post(self, request, invite_id):
        invite = get_object_or_404(AccountInvite, pk=invite_id, inviter=request.user, accepted=True)
        if invite.accepted_by:
            from cactus_cat_software.projects.models import Project
            for project in Project.objects.filter(client=request.user):
                project.collaborators.remove(invite.accepted_by)
        invite.delete()
        return JsonResponse({"success": True})


remove_team_member_view = RemoveTeamMemberView.as_view()


class AcceptInviteView(LoginRequiredMixin, View):
    """Accept a team invite. LoginRequired redirects to login then back here."""

    def get(self, request, token):
        invite = get_object_or_404(AccountInvite, token=token, accepted=False)

        invite.accepted = True
        invite.accepted_by = request.user
        invite.save()

        from cactus_cat_software.projects.models import Project
        for project in Project.objects.filter(client=invite.inviter):
            project.collaborators.add(request.user)

        messages.success(
            request,
            f"You now have access to {invite.inviter.name or invite.inviter.email}'s projects.",
        )
        return redirect("projects:dashboard")


accept_invite_view = AcceptInviteView.as_view()
