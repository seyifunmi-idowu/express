import requests
from django.conf import settings


class OneSignalIntegration:

    secret_key = settings.ONE_SIGNAL_KEY
    app_id = settings.ONE_SIGNAL_APP_ID
    headers = {
        "Authorization": f"Basic {secret_key}",
        "Content-Type": "application/json",
    }
    base_url = "https://onesignal.com/api/v1/"

    @classmethod
    def create_notification(cls,):
        data = {
            "app_id": cls.app_id,
            "include_aliases": {
                "external_id": [
                    "custom-external_id-assigned-by-api"
                ],  # send either external_id or onesignal_id
                "onesignal_id": ["custom-onesignal_id-assigned-by-api"],
            },
            "contents": {"en": "Sample Push Message"},
        }
        url = f"{cls.base_url}notifications"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()
