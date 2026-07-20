from django import forms

TIMELINE_CHOICES = [
    ("", "Select a timeline…"),
    ("asap", "As soon as possible"),
    ("1_month", "Within 1 month"),
    ("1_3_months", "1 – 3 months"),
    ("3_6_months", "3 – 6 months"),
    ("flexible", "Flexible / just exploring"),
]


class QuoteRequestForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Email Address")
    budget_range = forms.CharField(
        max_length=100,
        label="Starting Budget",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Starting at $5,000"}),
    )
    goals = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "What problem are you solving or outcome are you after?"}),
        label="Goals",
    )
    timeline = forms.ChoiceField(choices=TIMELINE_CHOICES, label="Timeline")
    service_name = forms.CharField(widget=forms.HiddenInput)
