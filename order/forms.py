from django import forms

from order.models import Order, Vehicle


class VehicleAdminForm(forms.ModelForm):

    ACTION_CHOICES = (
        ("", "Select action"),
        ("CHECK_PRICE", "Calculate price"),
        ("CHANGE_VEHICLE_IMAGE", "Change vehicle image"),
    )
    action = forms.ChoiceField(choices=ACTION_CHOICES, required=False)
    start_address = forms.CharField(required=False)
    end_address = forms.CharField(required=False)
    vehicle_image = forms.ImageField(required=False, help_text="Change vehicle image")

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")
        start_address = cleaned_data.get("start_address")
        end_address = cleaned_data.get("end_address")
        vehicle_image = cleaned_data.get("vehicle_image")

        if action == "CHECK_PRICE":
            if not start_address or not end_address:
                self.add_error(
                    "start_address",
                    "Start address and end address are required for price calculation.",
                )

        elif action == "CHANGE_VEHICLE_IMAGE":
            if not vehicle_image:
                self.add_error(
                    "vehicle_image", "Vehicle image is required for changing the image."
                )

    class Meta:
        model = Vehicle
        fields = "__all__"


class OrderAdminForm(forms.ModelForm):
    ACTION_CHOICES = (("", "Select action"), ("CANCEL_ORDER", "Cancel order"))
    action = forms.ChoiceField(choices=ACTION_CHOICES, required=False)
    reason = forms.CharField(
        required=False,
        help_text="Reason for action selected e.g reason for cancelling order",
    )

    class Meta:
        model = Order
        fields = "__all__"
