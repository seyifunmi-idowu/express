from django import forms

from authentication.models import User
from helpers.validators import FieldValidators


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Your password can't be too similar to your other personal information."
        "<br /> Your password must contain at least 8 characters."
        "<br /> Your password can't be  a commonly used password."
        "<br /> Your password can't be entirely numeric.",
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_password2(self):
        import re

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        reg_ex_rule = re.compile(FieldValidators.PASSWORD_REGEX_RULE)

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if not reg_ex_rule.search(password2):
            raise forms.ValidationError(
                "Password should be aleast 8-32 characters long and should contain upper, lower case letters and numbers"
            )
        return password2

    def save(self, commit=True):
        instance = super(CreateUserForm, self).save(commit=False)
        instance.set_password(self.cleaned_data["password2"])
        instance.email_verified = True
        instance.user_type = "ADMIN"
        if commit:
            instance.save()
        return instance

    class Meta:
        model = User
        fields = "__all__"
