from django import forms

from order.models import Vehicle


class VehicleAdminForm(forms.ModelForm):
    vehicle_image = forms.ImageField(required=False, help_text="Change vehicle image")

    class Meta:
        model = Vehicle
        fields = "__all__"
