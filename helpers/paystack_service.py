import requests
from django.conf import settings


class PaystackService:

    secret_key = settings.PAYSTACK_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    base_url = "https://api.paystack.co/"

    @classmethod
    def verify_account_number(cls, bank_code, acc_number):
        url = f"{cls.base_url}bank/resolve?account_number={acc_number}&bank_code={bank_code}"
        response = requests.get(url, headers=cls.headers)
        return response.json()

    @classmethod
    def get_banks(cls):
        url = f"{cls.base_url}bank"
        response = requests.get(url, headers=cls.headers)
        return response.json()

    @classmethod
    def create_transfer_recipient(cls, data):
        url = f"{cls.base_url}transferrecipient"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def initiate_transfer(cls, data):
        url = f"{cls.base_url}transfer"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def create_payment_page(cls, data):
        url = f"{cls.base_url}page"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def verify_transaction(cls, reference):
        url = f"{cls.base_url}transaction/verify/{reference}"
        response = requests.get(url, headers=cls.headers)
        return response.json()

    @classmethod
    def initialize_payment(cls, email, amount, currency="NGN", callback_url=None):
        data = {
            "email": email,
            "amount": amount * 100,
            "currency": currency,
            "callback_url": callback_url,
        }
        url = f"{cls.base_url}transaction/initialize"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()

    @classmethod
    def charge_card(cls, email, amount, card_auth=None):
        data = {"email": email, "amount": amount * 100, "authorization_code": card_auth}
        url = f"{cls.base_url}transaction/charge_authorization"
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()
