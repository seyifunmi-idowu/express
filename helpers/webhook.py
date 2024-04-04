import requests

from business.service import BusinessService
from helpers.logger import CustomLogging
from order.serializers import BusinessOrderSerializer


class FeleWebhook:
    @classmethod
    def send_order_to_webhook(cls, order):
        url = order.business.webhook_url
        secret_key = BusinessService.get_business_user_secret_key(order.business.user)
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        data = BusinessOrderSerializer(order).data
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.json()

        except Exception as e:
            CustomLogging.error(
                f"Unable to connect to webhook url {url}: {str(e)}", data
            )
            pass
