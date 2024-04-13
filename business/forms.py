from django import forms

from helpers.validators import FormValidator


class BusinessRegistrationForm(forms.Form):

    business_name = forms.CharField(required=True)
    email = forms.EmailField(
        required=True, validators=[FormValidator.validate_non_existing_user_email]
    )
    phone_number = forms.CharField(
        min_length=10,
        max_length=15,
        validators=[
            FormValidator.validate_phone_number,
            FormValidator.validate_non_existing_user_phone,
        ],
        required=True,
    )
    password = forms.CharField(validators=[FormValidator.validate_password])
    verify_password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        verify_password = cleaned_data.get("verify_password")

        if password and verify_password and password != verify_password:
            self.add_error("verify_password", "Passwords do not match.")

        return cleaned_data


class VerifyEmailForm(forms.Form):
    code = forms.CharField(max_length=6)
    email = forms.EmailField(
        required=False, validators=[FormValidator.validate_existing_user_email]
    )
    phone_number = forms.CharField(
        min_length=10,
        max_length=15,
        validators=[
            FormValidator.validate_phone_number,
            FormValidator.validate_existing_user_phone,
        ],
        required=False,
    )

    def validate(self, data):
        FormValidator.validate_email_or_phone_number(data)
        return data


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True, validators=[FormValidator.validate_existing_user_email]
    )
    password = forms.CharField()


class SubmitWebhookUrlForm(forms.Form):
    webhook_url = forms.URLField(required=True, validators=[FormValidator.validate_url])


class FundWalletForm(forms.Form):
    amount = forms.IntegerField(required=True)
