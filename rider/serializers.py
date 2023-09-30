from rest_framework import serializers, status

from helpers.validators import FieldValidators


class RiderSignupSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    email = serializers.EmailField(
        validators=[FieldValidators.validate_non_existing_user_email]
    )
    phone_number = serializers.CharField(
        min_length=10,
        max_length=15,
        validators=[
            FieldValidators.validate_phone_number,
            FieldValidators.validate_non_existing_user_phone,
        ],
        required=True,
    )
    address = serializers.CharField()
    VEHICLE_TYPE_CHOICES = [
        ("BICYCLE", "BICYCLE"),
        ("CAR", "CAR (SEDAN)"),
        ("KEKE", "KEKE"),
        ("MOTORCYCLE", "MOTORCYCLE"),
        ("MPV", "MPV (MULTI-PURPOSE VAN)"),
        ("TRUCKS", "TRUCKS"),
    ]
    CITY_CHOICES = [("MAKURDI", "MAKURDI"), ("GBOKO", "GBOKO"), ("OTUKPO", "OTUKPO")]
    vehicle_type = serializers.ChoiceField(choices=VEHICLE_TYPE_CHOICES)
    city = serializers.ChoiceField(choices=CITY_CHOICES)
    password = serializers.CharField(validators=[FieldValidators.validate_password])
    verify_password = serializers.CharField()

    def validate(self, data):
        fullname = data.get("fullname")
        fullname_split = fullname.split()
        if len(fullname_split) != 2:
            raise serializers.ValidationError(
                "Full name must contain first name and last name."
            )

        password = data.get("password")
        verify_password = data.get("verify_password")
        if password != verify_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data


class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    email = serializers.EmailField(
        required=False, validators=[FieldValidators.validate_existing_user_email]
    )
    phone_number = serializers.CharField(
        min_length=10,
        max_length=15,
        validators=[
            FieldValidators.validate_phone_number,
            FieldValidators.validate_existing_user_phone,
        ],
        required=False,
    )

    def validate(self, data):
        email = data.get("email")
        phone_number = data.get("phone_number")

        if email is None and phone_number is None:
            raise serializers.ValidationError("Provide an email or phone_number")
        elif email and phone_number:
            raise serializers.ValidationError("Provide only an email or phone_number")

        return data
