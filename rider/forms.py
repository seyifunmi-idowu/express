from django import forms

from rider.models import Rider


class RiderActionForm(forms.ModelForm):
    ACTION_CHOICES = (
        ("", "Select action"),
        ("APPROVE_RIDER", "Approve rider"),
        ("DISAPPROVE_RIDER", "Disapprove rider"),
        ("SUSPEND_RIDER", "Suspend rider"),
    )
    CITY_CHOICES = (
        ("", "Select rider city"),
        ("MAKURDI", "MAKURDI"),
        ("GBOKO", "GBOKO"),
        ("OTUKPO", "OTUKPO"),
    )
    action = forms.ChoiceField(choices=ACTION_CHOICES, required=False)
    decline_reason = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.ChoiceField(choices=CITY_CHOICES)

    class Meta:
        model = Rider
        fields = "__all__"
