from rest_framework import serializers, status

from authentication.models import User
from helpers.validators import FieldValidators


class UserProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField("get_display_name")
    is_rider = serializers.SerializerMethodField("get_is_rider")
    is_customer = serializers.SerializerMethodField("get_is_customer")

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "phone_number",
            "phone_verified",
            "street_address",
            "city",
            "last_login",
            "is_rider",
            "is_customer",
            "display_name",
        )

    def get_is_rider(self, obj):
        return obj.user_type == "RIDER"

    def get_is_customer(self, obj):
        return obj.user_type == "CUSTOMER"

    def get_display_name(self, obj):
        return obj.display_name

