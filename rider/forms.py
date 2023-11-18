from django import forms

from rider.models import Rider


class RiderActionForm(forms.ModelForm):
    ACTION_CHOICES = (
        ("", "Select action"),
        ("APPROVE_RIDER", "Approve rider"),
        ("DISAPPROVE_RIDER", "Disapprove rider"),
        ("SUSPEND_RIDER", "Suspend rider"),
    )
    action = forms.ChoiceField(choices=ACTION_CHOICES, required=False)

    class Meta:
        model = Rider
        fields = "__all__"
