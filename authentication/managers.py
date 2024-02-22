from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Manager Class for User Model"""

    def create_user(self, **kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        email = kwargs.get("email")
        password = kwargs.get("password")
        phone_number = kwargs.get("phone_number")
        user_type = kwargs.get("user_type")
        is_staff = kwargs.get("is_staff")
        referral_code = kwargs.get("referral_code")
        user = self.model(
            first_name=first_name.capitalize() if first_name else None,
            last_name=last_name.capitalize() if last_name else None,
            email=self.normalize_email(email),
            phone_number=phone_number,
            referral_code=referral_code,
        )
        if password:
            user.set_password(password)
        if user_type:
            user.user_type = user_type
        if is_staff:
            user.is_staff = is_staff
        user.save()

        return user

    def create_staffuser(
        self, first_name, last_name, email, password, phone_number=None
    ):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            user_type="ADMIN",
            phone_number=phone_number,
        )
        user.email_verified = True
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            user_type="ADMIN",
        )
        user.email_verified = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
