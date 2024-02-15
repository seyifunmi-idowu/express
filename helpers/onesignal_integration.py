import requests
from django.conf import settings


class OneSignalIntegration:

    secret_key = settings.ONE_SIGNAL_KEY
    app_id = settings.ONE_SIGNAL_APP_ID
    sms_from = settings.ONE_SIGNAL_SMS_FROM
    app_env = settings.ENVIRONMENT
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

    @classmethod
    def add_sms_device(cls, phone_number, user_id, first_name=None, last_name=None):
        data = {
            "device_type": 14,
            "tags": {"first_name": first_name, "last_name": last_name},
            "app_id": cls.app_id,
            "identifier": phone_number,
            "test_type": "1" if cls.app_env == "production" else "2",
            "language": "en",
            "external_user_id": user_id,
            "timezone": "3600",
            "notification_types": 1,
            "country": "NG",
            "timezone_id": "Africa/Lagos",
        }
        url = f"{cls.base_url}players"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def delete_sms_device(cls, subscription_id):
        url = f"{cls.base_url}players/{subscription_id}?app_id={cls.app_id}"
        response = requests.delete(url, headers=cls.headers)
        return response.json()

    @classmethod
    def send_sms_notification(cls, phone_number, message):
        data = {
            "app_id": cls.app_id,
            "name": "Fele-Express",
            "sms_from": cls.sms_from,
            "contents": {"en": message},
            "include_phone_numbers": [phone_number],
        }
        url = f"{cls.base_url}notifications"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def send_push_notification(cls, subscription_list, title, message):
        data = {
            "app_id": cls.app_id,
            "include_subscription_ids": subscription_list,
            "contents": {"en": message},
            "headings": {"en": title},
        }
        url = f"{cls.base_url}notifications"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()
