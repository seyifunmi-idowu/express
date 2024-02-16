from django.core.management.base import BaseCommand

from authentication.models import User
from helpers.db_helpers import generate_referral_code


class Command(BaseCommand):
    """
    This postfix is to add referral code to users.
    """

    def handle(self, *args, **kwargs):
        users_qs = User.objects.filter(referral_code__isnull=True)

        self.stdout.write(
            self.style.WARNING(
                f"Initializing Postfix to add referral code for {users_qs.count()} users..."
            )
        )
        admin_users_affected = 0
        for user in users_qs:
            admin_users_affected += 1
            user.referral_code = generate_referral_code()
            user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed Postfix to add referral code for {admin_users_affected} users."
            )
        )
