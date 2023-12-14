from django.conf import settings


class OneSignalService:

    secret_key = settings.ONE_SIGNAL_KEY
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    base_url = "https://api.paystack.co/"

    @classmethod
    def create_user(cls, user_id, data):
        """
        Keyword arguments:
        argument:
            data -> {
                "user_id": user identity,
            }
            user -> user object
        Return: credit_record object
       """
