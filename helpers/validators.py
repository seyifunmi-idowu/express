import os
from typing import List

import phonenumbers
from django import forms
from django.conf import settings
from rest_framework import serializers, status

from authentication.models import User
from helpers.exceptions import CustomAPIException
from helpers.nigeria_states_and_capital import NIGERIA_STATES_AND_CAPITAL
from helpers.nigerian_phonenumbers import NigerianPhone


class FieldValidators:
    """Field validator class for serializer fields"""

    PASSWORD_REGEX_RULE = "^(?=.*([A-Z]){1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,})(?=.*[a-z]{1,})(?=.*[!\"#$%&'()*+,-./:;<=>?@^_`{|}~]{0,}).{8,32}$"
    HTTPS_URL_REGEX_RULE = r"^https:\/\/[^\s\/$.?#].[^\s]*$"

    @staticmethod
    def validate_non_existing_user_email(email_address: str) -> None:
        user = User.objects.filter(email__iexact=email_address.lower()).first()
        if user:
            raise serializers.ValidationError(
                "A user has already registered with this email address"
            )

    @staticmethod
    def validate_non_existing_user_phone(phone_number: str) -> None:
        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            raise serializers.ValidationError(
                "A user has already registered with this phone number"
            )

    @staticmethod
    def validate_existing_user_email(email_address: str) -> None:
        user = User.objects.filter(email__iexact=email_address.lower()).first()
        if not user:
            raise serializers.ValidationError("User with email address not found")

    @staticmethod
    def validate_existing_user_phone(phone_number: str) -> None:
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise serializers.ValidationError("User with phone number not found")

    @staticmethod
    def validate_phone_number(phone_number: str) -> None:
        try:
            # This will validate all international numbers
            validated_no = phonenumbers.parse(phone_number)
            if str(validated_no.country_code) == "234":
                phone = NigerianPhone(phone_number)
                if not phone.is_valid():
                    raise serializers.ValidationError("Phone number is not valid")
            else:
                if phonenumbers.is_valid_number(validated_no) is False:
                    raise serializers.ValidationError("Phone number is not valid")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("Phone number is not valid")

    @staticmethod
    def validate_password(password: str) -> None:
        """Runs a validation check on user-provided password"""
        import re

        reg_ex_rule = re.compile(FieldValidators.PASSWORD_REGEX_RULE)

        if not reg_ex_rule.search(password):
            raise serializers.ValidationError(
                "Password should be at least 8-32 characters and should contain upper, lower case letters, numbers and special characters"
            )

    @staticmethod
    def _validate_file_extension(value, valid_extensions):
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        if ext.lower() not in valid_extensions:
            raise serializers.ValidationError("File type is not supported")

    @staticmethod
    def validate_file_extension(value):
        FieldValidators._validate_file_extension(
            value, [".pdf", ".png", ".jpg", ".jpeg"]
        )

    @staticmethod
    def validate_resume_file_extension(value):
        FieldValidators._validate_file_extension(value, [".pdf", ".doc", ".docx"])

    @staticmethod
    def validate_bank_statement_file_extension(value):
        FieldValidators._validate_file_extension(
            value, [".pdf", ".csv", ".xls", ".xlsx"]
        )

    @staticmethod
    def validate_file_size(value):
        if value.size > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError("File can not be larger than 3MB")

    @staticmethod
    def validate_business_registration_number(number: str) -> None:
        """
        Runs validation to ensure the number given fits the criteria
        of a Nigerian business number
        """
        import re

        if not re.fullmatch(r"^(BN|RC|LP|IT|LLP)?[0-9]{6,10}$", number):
            raise serializers.ValidationError("Business registration number is invalid")

    @staticmethod
    def validate_bvn(number: str) -> None:
        """
        Runs a validation check on a given bank verification number
        """
        import re

        reg_ex_rule = re.compile("^[0-9]{11}$")
        if not reg_ex_rule.search(number):
            raise serializers.ValidationError("Bank Verification Number is invalid")

    @staticmethod
    def validate_email_or_phone_number(data):
        email = data.get("email")
        phone_number = data.get("phone_number")

        if not email and not phone_number:
            raise serializers.ValidationError(
                "Either email or phone number is required"
            )

        if email and phone_number:
            raise serializers.ValidationError(
                "Only one of email or phone number can be submitted at a time"
            )

    @staticmethod
    def validate_local_government_area(lga: str, state: str) -> bool:
        state_lgas: List[str] = NIGERIA_STATES_AND_CAPITAL.get(state, [])
        if lga.lower() in [lga.lower() for lga in state_lgas]:
            return True
        raise serializers.ValidationError(
            "This LGA does not belong to the selected state."
        )


class NonSerializerInputValidator:
    """
    This class contain methods that validate input that won't be serialized
    e.g django admin form input
    """

    @staticmethod
    def validate_existing_user_email(email: str) -> bool:
        return User.objects.filter(email__iexact=email).exists()

    @staticmethod
    def validate_admin_user(user) -> bool:
        user_types_list = ["ADMIN", "USER_SERVICE", "GROWTH", "FINANCE", "DEVELOPER"]

        return True if user.user_type in user_types_list else False


class Validators:
    @staticmethod
    def is_start_date_less_than_or_equals_end_date(start_date, end_date):
        """
        Validate that the end date is greater than or equal to the start date
        """
        from django.utils import dateparse

        start_date = dateparse.parse_date(start_date)
        end_date = dateparse.parse_date(end_date)

        if end_date >= start_date:
            return True

        raise CustomAPIException(
            detail="The end date should be greater than or equal to the start date.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class FormValidator:
    """Form validator class for form fields"""

    @staticmethod
    def validate_non_existing_user_email(email_address: str) -> None:
        user = User.objects.filter(email__iexact=email_address.lower()).first()
        if user:
            raise forms.ValidationError(
                "A user has already registered with this email address"
            )

    @staticmethod
    def validate_non_existing_user_phone(phone_number: str) -> None:
        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            raise forms.ValidationError(
                "A user has already registered with this phone number"
            )

    @staticmethod
    def validate_existing_user_email(email_address: str) -> None:
        user = User.objects.filter(email__iexact=email_address.lower()).first()
        if not user:
            raise forms.ValidationError("User with email address not found")

    @staticmethod
    def validate_existing_user_phone(phone_number: str) -> None:
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise forms.ValidationError("User with phone number not found")

    @staticmethod
    def validate_phone_number(phone_number: str) -> None:
        try:
            # This will validate all international numbers
            validated_no = phonenumbers.parse(phone_number)
            if str(validated_no.country_code) == "234":

                phone = NigerianPhone(phone_number)
                if not phone.is_valid():
                    raise forms.ValidationError("Phone number is not valid")
            else:
                if phonenumbers.is_valid_number(validated_no) is False:

                    raise forms.ValidationError("Phone number is not valid")
        except phonenumbers.phonenumberutil.NumberParseException:
            phone = NigerianPhone(phone_number)
            if not phone.is_valid():
                raise forms.ValidationError("Phone number is not valid")

    @staticmethod
    def validate_password(password: str) -> None:
        """Runs a validation check on user-provided password"""
        import re

        reg_ex_rule = re.compile(FieldValidators.PASSWORD_REGEX_RULE)

        if not reg_ex_rule.search(password):
            raise forms.ValidationError(
                "Password should be at least 8-32 characters and should contain upper, lower case letters, numbers and special characters"
            )

    @staticmethod
    def validate_email_or_phone_number(data):
        email = data.get("email")
        phone_number = data.get("phone_number")

        if not email and not phone_number:
            raise forms.ValidationError("Either email or phone number is required")

        if email and phone_number:
            raise forms.ValidationError(
                "Only one of email or phone number can be submitted at a time"
            )

    @staticmethod
    def validate_url(url: str) -> None:
        import re

        """Runs a validation check on user-provided URL"""
        reg_ex_rule = re.compile(FieldValidators.HTTPS_URL_REGEX_RULE)

        if not reg_ex_rule.match(url):
            raise forms.ValidationError(
                "Invalid URL. Please provide a valid URL starting with 'http://' or 'https://'."
            )
