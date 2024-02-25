from django import forms

from notification.models import Notification


class NotificationActionForm(forms.ModelForm):
    DELIVERY_TYPE__CHOICES = (
        ("", "Select action"),
        ("PUSH", "Push notification"),
        ("SILENT", "Silent notification"),
    )
    delivery_type = forms.ChoiceField(choices=DELIVERY_TYPE__CHOICES, required=False)

    class Meta:
        model = Notification
        fields = "__all__"
