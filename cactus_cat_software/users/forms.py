from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from .models import AccountInvite, NewsletterSubscriber, User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.AdminUserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    marketing_opt_in = forms.BooleanField(
        required=False,
        label=_("Yes, I want to receive personalized updates and offers from Cactus Cat Software"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password1" in self.fields:
            self.fields["password1"].help_text = ""
        if "marketing_opt_in" in self.fields:
            self.fields["marketing_opt_in"] = self.fields.pop("marketing_opt_in")

    def custom_signup(self, request, user):
        if self.cleaned_data.get("marketing_opt_in"):
            NewsletterSubscriber.objects.get_or_create(email=user.email)


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

    marketing_opt_in = forms.BooleanField(
        required=False,
        label=_("Yes, I want to receive personalized updates and offers from Cactus Cat Software"),
    )

    def custom_signup(self, request, user):
        if self.cleaned_data.get("marketing_opt_in"):
            NewsletterSubscriber.objects.get_or_create(email=user.email)


class BusinessInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "company_name", "phone_number", "website"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Your name"}),
            "company_name": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Company name"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Phone number"}),
            "website": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "https://"}),
        }


class InviteForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "coworker@company.com",
        }),
    )

    def __init__(self, inviter, *args, **kwargs):
        self.inviter = inviter
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if email == self.inviter.email.lower():
            raise forms.ValidationError("You cannot invite yourself.")
        if AccountInvite.objects.filter(inviter=self.inviter, email=email, accepted=False).exists():
            raise forms.ValidationError("An invite is already pending for this email.")
        if AccountInvite.objects.filter(inviter=self.inviter, email=email, accepted=True).exists():
            raise forms.ValidationError("This person already has access to your account.")
        return email
